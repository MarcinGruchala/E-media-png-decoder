import zlib
import cv2
import numpy as np
import matplotlib.pyplot as plt
from IHDR import IHDR, struct
from IDAT import IDAT

def read_chunk(file):
    chunkLength, chunkType = struct.unpack('>I4s', file.read(8))
    chunkData = file.read(chunkLength)
    checksum = zlib.crc32(chunkData, zlib.crc32(struct.pack('>4s', chunkType)))
    chunk_crc, = struct.unpack('>I', file.read(4))
    if chunk_crc != checksum:
        raise Exception('chunk checksum failed {} != {}'.format(chunk_crc,
            checksum))
    return chunkType, chunkData

class Decoder:
    PNG_SIGNATURE = b'\x89PNG\r\n\x1a\n'

    def __init__(self, image,cvImg):
        self.img = image
        self.cvImg = cvImg
        self.chunks = []
        while True:
            chunkType, chunkData = read_chunk(self.img)
            self.chunks.append((chunkType, chunkData))
            if chunkType == b'IEND':
                break
        self.IHDR = self.readIHDR()
        self.IDAT = self.readIDAT()
        self.bytesPerPixel = self.getBytesPerPixel()

    def readIHDR(self):
        return IHDR(self.chunks[0][1])

    def readIDAT(self):
        idatData = b''.join(chunk_data for chunk_type, chunk_data in self.chunks if chunk_type == b'IDAT')
        return IDAT(idatData,self.getBytesPerPixel(),self.IHDR.width,self.IHDR.height)

    def getBytesPerPixel(self):
        if(self.IHDR.colorType == 0):
            return 1
        elif(self.IHDR.colorType == 2):
            return 3
        elif(self.IHDR.colorType == 3):
            return 1
        elif(self.IHDR.colorType == 4):
            return 2
        elif(self.IHDR.colorType == 6):
            return 4
        else:
            return -1

    def printChunks(self):
        print([chunkType for chunkType, chunkData in self.chunks])

    def printMetedata(self):
        print("Chunks: ")
        self.printChunks()
        print("\nImage atributes: ")
        self.IHDR.printInformations()
        print(f'Bytes per pixel: {self.bytesPerPixel}')

    def showIDAT(self):
        self.IDAT.reconstructsPixelData()
        self.IDAT.show()

    def showFFT(self):
        beforFFT = self.cvImg
        fft = np.fft.fft2(self.cvImg)
        fftCentered = np.fft.fftshift(fft)
        fftDecentered = np.fft.ifftshift(fftCentered)
        invertFFt = np.fft.ifft2(fftDecentered)
        plt.subplot(221), plt.imshow(beforFFT, 'gray'), plt.title("Orgiinal Image in grayscale")
        plt.subplot(222), plt.imshow(np.log(1+np.abs(fft)), "gray"), plt.title("Spectrum")
        plt.subplot(223), plt.imshow(np.log(1+np.abs(fftCentered)), "gray"), plt.title("Centered Spectrum")
        plt.subplot(224), plt.imshow(np.abs(invertFFt), "gray"), plt.title("Image after iverse FFT")
        plt.show()

