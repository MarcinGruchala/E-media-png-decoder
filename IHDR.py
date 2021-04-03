import struct

class IHDR:
    def __init__(self, chunkData):
        self.width = struct.unpack('>IIBBBBB', chunkData)[0]
        self.height = struct.unpack('>IIBBBBB', chunkData)[1]
        self.bitDepth = struct.unpack('>IIBBBBB', chunkData)[2]
        self.colorType = struct.unpack('>IIBBBBB', chunkData)[3]
        self.compressionMethod = struct.unpack('>IIBBBBB', chunkData)[4]
        self.filterMethod = struct.unpack('>IIBBBBB', chunkData)[5]
        self.interlaceMethod = struct.unpack('>IIBBBBB', chunkData)[6]

    def printNice(self):
        print(f'\nIHDR:')
        print(f'Width: {self.width}\nHeight: {self.height}\nBit Depth: {self.bitDepth}\nColor type: {self.colorType}')
        print(f'Compression Method: {self.compressionMethod}\nFilter Method: {self.filterMethod}')
        print(f'Interlace Method: {self.interlaceMethod}')
