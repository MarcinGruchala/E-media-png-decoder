import zlib
import cv2
import numpy as np
import matplotlib.pyplot as plt
import copy
from PIL import Image
from IHDR import IHDR, struct
from IDAT import IDAT
from PLTE import PLTE
from Chunk import Chunk

def read_chunk(file):
    chunkLength, chunkType = struct.unpack('>I4s', file.read(Chunk.LENGTH_BYTES+Chunk.TYPE_BYTES))
    chunkData = file.read(chunkLength)
    checksum = zlib.crc32(chunkData, zlib.crc32(struct.pack('>4s', chunkType)))
    chunkCrc, = struct.unpack('>I', file.read(Chunk.CRC_BYTES))
    if chunkCrc != checksum:
        raise Exception('chunk checksum failed {} != {}'.format(chunkCrc,
            checksum))
    return Chunk(chunkLength,chunkType,chunkData,chunkCrc)

class Decoder:
    PNG_SIGNATURE = b'\x89PNG\r\n\x1a\n'
    CRITICAL_CHUNKS = [b'IHDR',b'PLTE',b'IDAT',b'IEND']

    def __init__(self, image,cvImg):
        self.img = image
        self.cvImg = cvImg
        self.chunks = []
        while True:
            chunk = read_chunk(self.img)
            self.chunks.append(chunk)
            if chunk.type == b'IEND':
                break
        self.IHDR = self.readIHDR()
        self.PLTE = self.readPLTE()
        self.IDAT = self.readIDAT()
        self.bytesPerPixel = self.getBytesPerPixel()
        self.stride = self.IHDR.width * self.bytesPerPixel
        self.reconstructedPixelData = []
        self.reconstructsPixelData()


    def readIHDR(self):
        return IHDR(self.chunks[0].data)

    def readPLTE(self):
        for chunk in self.chunks:
            if(chunk.type == b'PLTE'):
                return PLTE(chunk.data)
        return PLTE(b'')

    def readIDAT(self):
        idatData = b''.join(chunk.data for chunk in self.chunks if chunk.type == b'IDAT')
        return IDAT(idatData)

    def getBytesPerPixel(self):
        if(self.IHDR.colorType == 0): return 1
        elif(self.IHDR.colorType == 2): return 3
        elif(self.IHDR.colorType == 3): return 1
        elif(self.IHDR.colorType == 4): return 2
        elif(self.IHDR.colorType == 6): return 4
        else: return -1

    def printChunks(self):
        print([chunk.type for chunk in self.chunks])

    def showImg(self):
        Image.open(self.img).show()

    def showMetedata(self):
        print("Chunks: ")
        self.printChunks()
        print("\nImage atributes: ")
        self.IHDR.printInformations()
        print(f'Bytes per pixel: {self.bytesPerPixel}')

    def showFFT(self):
        beforFFT = self.cvImg
        fft = np.fft.fft2(self.cvImg)
        fftCentered = np.fft.fftshift(fft)
        fftDecentered = np.fft.ifftshift(fftCentered)
        invertFFt = np.fft.ifft2(fftDecentered)
        plt.subplot(221), plt.imshow(beforFFT, 'gray'), plt.title("Orgiinal Image in grayscale")
        plt.subplot(222), plt.imshow(np.log(1+np.abs(fft)), "gray"), plt.title("Spectrum")
        plt.subplot(223), plt.imshow(np.log(1+np.abs(fftCentered)), "gray"), plt.title("Centered Spectrum")
        plt.subplot(224), plt.imshow(np.abs(invertFFt), "gray"), plt.title("Image after inverse FFT")
        plt.show()

    def showPixelData(self):
        plt.imshow(np.array(self.reconstructedPixelData).reshape((self.IHDR.height, self.IHDR.width, self.bytesPerPixel)))
        plt.show()

    def showPLTEPalette(self):
        paletteGraf = np.array(self.PLTE.palette)
        i = np.arange(256).reshape(16,16)
        plt.imshow(paletteGraf[i])
        plt.show()

    def paethPredictor(self,a, b, c):
        p = a + b - c
        pa = abs(p - a)
        pb = abs(p - b)
        pc = abs(p - c)
        if pa <= pb and pa <= pc:
            Pr = a
        elif pb <= pc:
            Pr = b
        else:
            Pr = c
        return Pr

    def reconstructedPixelData_a(self, r, c):
        return self.reconstructedPixelData[r * self.stride + c - self.bytesPerPixel] if c >= self.bytesPerPixel else 0

    def reconstructedPixelData_b(self, r, c):
        return self.reconstructedPixelData[(r-1) * self.stride + c] if r > 0 else 0

    def reconstructedPixelData_c(self, r, c):
        return self.reconstructedPixelData[(r-1) * self.stride + c - self.bytesPerPixel] if r > 0 and c >= self.bytesPerPixel else 0

    def reconstructsPixelData(self):
        i = 0
        for r in range(self.IHDR.height): # for each scanline
            filter_type = self.IDAT.decompressedData[i] # first byte of scanline is filter type
            i += 1
            for c in range(self.stride): # for each byte in scanline
                Filt_x = self.IDAT.decompressedData[i]
                i += 1
                if filter_type == 0: # None
                    reconstructedPixelData_x = Filt_x
                elif filter_type == 1: # Sub
                    reconstructedPixelData_x = Filt_x + self.reconstructedPixelData_a(r, c)
                elif filter_type == 2: # Up
                    reconstructedPixelData_x = Filt_x + self.reconstructedPixelData_b(r, c)
                elif filter_type == 3: # Average
                    reconstructedPixelData_x = Filt_x + (self.reconstructedPixelData_a(r, c) + self.reconstructedPixelData_b(r, c)) // 2
                elif filter_type == 4: # Paeth
                    reconstructedPixelData_x = Filt_x + self.paethPredictor(self.reconstructedPixelData_a(r, c), self.reconstructedPixelData_b(r, c), self.reconstructedPixelData_c(r, c))
                else:
                    raise Exception('unknown filter type: ' + str(filter_type))
                self.reconstructedPixelData.append(reconstructedPixelData_x & 0xff) # truncation to byte

    def createImageFromCriticalChunks(self):
        fileName = "newPNGImage.png"
        newFile = open(fileName, 'wb')
        newFile.write(Decoder.PNG_SIGNATURE)
        for chunk in self.chunks:
            if chunk.type in Decoder.CRITICAL_CHUNKS:
                newFile.write(struct.pack('>I',chunk.length))
                newFile.write(chunk.type)
                newFile.write(chunk.data)
                newFile.write(struct.pack('>I',chunk.crc))
        newFile.close()

