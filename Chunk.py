class Chunk:
    LENGTH_BYTES = 4
    CHUNK_TYPE_BYTES = 4
    CRC_BYTES = 4
    def __init__(self,length,chunkType,data,crc):
        self.length = length
        self.type = chunkType
        self.data = data
        self.crc = crc

