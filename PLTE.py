from chunk import Chunk
class PLTE(Chunk):
    def __init__(self,length,chunkType,data,crc):
        super().__init__(length,chunkType,data,crc)
        self.palette = self.getPalette()

    def getPalette(self):
        palette = []
        for bytesIndex in range(0,len(self.data),3):
            pixel = self.data[bytesIndex:bytesIndex+3]
            pixelPalette = (pixel[0],pixel[1],pixel[2])
            palette.append(pixelPalette)
        return palette
