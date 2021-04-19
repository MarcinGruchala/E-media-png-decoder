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
from IDATDecoder import IDATDecoder


class Decoder:
    PNG_SIGNATURE = b'\x89PNG\r\n\x1a\n'
    CRITICAL_CHUNKS = [b'IHDR',b'PLTE',b'IDAT',b'IEND']

    def __init__(self, image,cvImg):
        self.img = image
        self.cvImg = cvImg
        self.chunks = self.readChunks()
        self.IHDR = self.readIHDR()
        self.bytesPerPixel = self.getBytesPerPixel()
        self.PLTE = self.readPLTE()
        self.IDATs = self.readIDATs()
        self.IDATDecoder = IDATDecoder(self.IDATs,self.IHDR.width, self.IHDR.height, self.bytesPerPixel)

    def read_chunk(self,file):
        chunkLength, chunkType = struct.unpack('>I4s', file.read(Chunk.LENGTH_BYTES+Chunk.TYPE_BYTES))
        chunkData = file.read(chunkLength)
        checksum = zlib.crc32(chunkData, zlib.crc32(struct.pack('>4s', chunkType)))
        chunkCrc, = struct.unpack('>I', file.read(Chunk.CRC_BYTES))
        if chunkCrc != checksum:
            raise Exception('chunk checksum failed {} != {}'.format(chunkCrc,
                checksum))
        return Chunk(chunkLength,chunkType,chunkData,chunkCrc)

    def readChunks(self):
        chunks = []
        while True:
            chunk = self.read_chunk(self.img)
            chunks.append(chunk)
            if chunk.type == b'IEND':
                break
        return chunks


    def readIHDR(self):
        return IHDR(self.chunks[0])

    def readPLTE(self):
        for chunk in self.chunks:
            if(chunk.type == b'PLTE'):
                return PLTE(chunk.length,chunk.type,chunk.data,chunk.crc)
        return PLTE(0,b'PLTE',b'',0)

    def readIDATs(self):
        return [IDAT(chunk) for chunk in self.chunks if chunk.type == b'IDAT']

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

    def printImageInformations(self):
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
        plt.imshow(np.array(self.IDATDecoder.reconstructedPixelData).reshape((self.IHDR.height, self.IHDR.width, self.bytesPerPixel)))
        plt.show()

    def showPLTEPalette(self):
        paletteGraf = np.array(self.PLTE.palette)
        i = np.arange(256).reshape(16,16)
        plt.imshow(paletteGraf[i])
        plt.show()

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

