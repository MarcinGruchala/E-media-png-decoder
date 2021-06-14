'''
File with IHDR chunk
'''
import struct
from chunk import Chunk
class IHDR(Chunk):
    '''
    Class represents IHDR chunk
    '''
    def __init__(self, chunk):
        super().__init__(chunk.length, chunk.type,chunk.data,chunk.crc)
        self.width = struct.unpack('>IIBBBBB', chunk.data)[0]
        self.height = struct.unpack('>IIBBBBB', chunk.data)[1]
        self.bit_depth = struct.unpack('>IIBBBBB', chunk.data)[2]
        self.color_type = struct.unpack('>IIBBBBB', chunk.data)[3]
        self.compression_method = struct.unpack('>IIBBBBB', chunk.data)[4]
        self.filter_method = struct.unpack('>IIBBBBB', chunk.data)[5]
        self.interlace_method = struct.unpack('>IIBBBBB', chunk.data)[6]

    def print_row_informations(self):
        '''
        Method prints row data information about IHDR chunk
        '''
        print(
            f'Width: {self.width}\n' +
            f'Height: {self.height}\n' +
            f'Bit Depth: {self.bit_depth}\n' +
            f'Color type: {self.color_type}')
        print(f'Compression Method: {self.compression_method}\nFilter Method: {self.filter_method}')
        print(f'Interlace Method: {self.interlace_method}')

    def print_informations(self):
        '''
        Method prints decoded information about IHDR chunk.
        '''
        print(f'Width: {self.width}\nHeight: {self.height}\nBit Depth: {self.bit_depth}')
        print(f'Color type: {self.get_color_type_name()}')
        print(f'Compression Method: {self.get_compression_method_name()}')
        print(f'Filter Method: {self.get_filter_method_name()}')
        print(f'Interlace Method: {self.get_interlace_method_name()}')

    def get_color_type_name(self):
        '''
        Method return colour type of image.
        '''
        if self.color_type == 0 :
            return "grayscale"
        if self.color_type == 2 :
            return "truecolor"
        if self.color_type == 3 :
            return "Indexed-color"
        if self.color_type == 4 :
            return "grayscale with alpha"
        if self.color_type == 6 :
            return "truecolor with alpha"

        return "ERROR: invalid color type"

    def get_compression_method_name(self):
        '''
        Method return compression method name.
        '''
        if self.compression_method == 0 :
            return "deflate/inflate compression with a sliding window of at most 32768 bytes"

        return "ERROR: invalid compression method"

    def get_filter_method_name(self):
        '''
        Method return filter method name.
        '''
        if self.filter_method == 0 :
            return "adaptive filtering with five basic filter types"

        return "ERROR: invalid filter method"

    def get_interlace_method_name(self):
        '''
        Method interlace method name.
        '''
        if self.interlace_method == 0 :
            return "no interlace"
        if self.interlace_method == 1 :
            return "Adam7 interlace"

        return "ERROR: invalid interlace method"
