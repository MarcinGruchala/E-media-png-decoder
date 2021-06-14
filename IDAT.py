'''
File with IDAT class
'''
from chunk import Chunk
class IDAT(Chunk):
    '''
    Class represents IDAT chunk
    '''
    def __init__(self, chunk):
        super().__init__(chunk.length, chunk.type,chunk.data,chunk.crc)
