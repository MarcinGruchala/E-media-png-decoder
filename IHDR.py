import struct
from chunk import Chunk
class IHDR(Chunk):
    def __init__(self, chunk):
        super().__init__(chunk.length, chunk.type,chunk.data,chunk.crc)
        self.width = struct.unpack('>IIBBBBB', chunk.data)[0]
        self.height = struct.unpack('>IIBBBBB', chunk.data)[1]
        self.bitDepth = struct.unpack('>IIBBBBB', chunk.data)[2]
        self.colorType = struct.unpack('>IIBBBBB', chunk.data)[3]
        self.compressionMethod = struct.unpack('>IIBBBBB', chunk.data)[4]
        self.filterMethod = struct.unpack('>IIBBBBB', chunk.data)[5]
        self.interlaceMethod = struct.unpack('>IIBBBBB', chunk.data)[6]

    def printRowInformations(self):
        print(f'Width: {self.width}\nHeight: {self.height}\nBit Depth: {self.bitDepth}\nColor type: {self.colorType}')
        print(f'Compression Method: {self.compressionMethod}\nFilter Method: {self.filterMethod}')
        print(f'Interlace Method: {self.interlaceMethod}')

    def printInformations(self):
        print(f'Width: {self.width}\nHeight: {self.height}\nBit Depth: {self.bitDepth}')
        print(f'Color type: {self.getColorTypeName()}')
        print(f'Compression Method: {self.getCimpressionMethodName()}')
        print(f'Filter Method: {self.getFilterMethodName()}')
        print(f'Interlace Method: {self.getInterlaceMethodName()}')

    def getColorTypeName(self):
        if(self.colorType == 0):
            return "grayscale"
        elif(self.colorType == 2):
            return "truecolor"
        elif(self.colorType == 3):
            return "Indexed-color"
        elif(self.colorType == 4):
            return "grayscale with alpha"
        elif(self.colorType == 6):
            return "truecolor with alpha"
        else:
            return "ERROR: invalid color type"

    def getCimpressionMethodName(self):
        if(self.compressionMethod == 0):
            return "deflate/inflate compression with a sliding window of at most 32768 bytes"
        else:
            return "ERROR: invalid compression method"

    def getFilterMethodName(self):
        if(self.filterMethod == 0):
            return "adaptive filtering with five basic filter types"
        else:
            return "ERROR: invalid filter method"

    def getInterlaceMethodName(self):
        if(self.interlaceMethod == 0):
            return "no interlace"
        elif(self.interlaceMethod == 1):
            return "Adam7 interlace"
        else:
            return "ERROR: invalid interlace method"
