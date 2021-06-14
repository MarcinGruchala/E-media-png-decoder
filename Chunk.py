'''
File with Chunk class.
'''
class Chunk:
    '''
    Class representing png data chunk.
    '''
    LENGTH_BYTES = 4
    TYPE_BYTES = 4
    CRC_BYTES = 4
    def __init__(self,length,chunkType,data,crc):
        self.length = length
        self.type = chunkType
        self.data = data
        self.crc = crc

    def print_row_data(self):
        '''
        Method prints row chunk data.
        '''
        print(self.data)

    def print_chunk_parameters(self):
        '''
        Method prints chunk parameters.
        '''
        print(f'Chunk type: {self.type} ')
        print(f"Length: {self.length}")
        print(f'Crc: {self.crc}')
        print(f'Row data: {self.data}')
