# import sys
import zlib
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

    def __init__(self, image):
        self.img = image
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
        self.idat = IDAT(idatData,self.ihdr.width,self.ihdr.height)

    def printChunks(self):
        print([chunkType for chunkType, chunkData in self.chunks])

    def printMetedata(self):
        self.ihdr.printInformations()

    def showIDAT(self):
        self.idat.reconstructsPixelData()
        self.idat.show()

