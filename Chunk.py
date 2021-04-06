class Chunk:
    def __init__(self,length,chunkType,data,crc):
        self.length = length
        self.type = chunkType
        self.data = data
        self.crc = crc

