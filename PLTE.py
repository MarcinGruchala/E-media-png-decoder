'''
File with PLTE class.
'''
from chunk import Chunk
class PLTE(Chunk):
    '''
    Class represents PLTE chunk
    '''
    def __init__(self,length,chunk_type,data,crc):
        super().__init__(length,chunk_type,data,crc)
        self.palette = self.get_palette()

    def get_palette(self):
        '''
        Method return colour palette
        '''
        palette = []
        for bytes_index in range(0,len(self.data),3):
            pixel = self.data[bytes_index:bytes_index+3]
            pixel_palette = (pixel[0],pixel[1],pixel[2])
            palette.append(pixel_palette)
        return palette
