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

    def readIHDR(self):
        self.ihdr = IHDR(self.chunks[0][1])

    def readIDAT(self):
        idatData = b''.join(chunk_data for chunk_type, chunk_data in self.chunks if chunk_type == b'IDAT')
        self.idat = IDAT(idatData,self.getBytesPerPixel(),self.ihdr.width,self.ihdr.height)

    def getBytesPerPixel(self):
        if(self.ihdr.colorType == 0):
            return 1
        elif(self.ihdr.colorType == 2):
            return 3
        elif(self.ihdr.colorType == 3):
            return -1
        elif(self.ihdr.colorType == 4):
            return 2
        elif(self.ihdr.colorType == 6):
            return 4
        else:
            return -1

    def printChunks(self):
        print([chunkType for chunkType, chunkData in self.chunks])

    def printMetedata(self):
        self.ihdr.printInformations()

    def showIDAT(self):
        self.idat.reconstructsPixelData()
        self.idat.show()

    def showFFT(self):
        # plt.imshow(self.cvImg,cmap='gray',vmin=0,vmax=255)
        fft = np.fft.fft2(self.cvImg)
        plt.imshow(np.log(1+np.abs(fft)), "gray")
        plt.show()

