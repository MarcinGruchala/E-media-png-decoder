class Chunk:
    LENGTH_BYTES = 4
    TYPE_BYTES = 4
    CRC_BYTES = 4
    def __init__(self,length,chunkType,data,crc):
        self.length = length
        self.type = chunkType
        self.data = data
        self.crc = crc

    def printRowData(self):
        print(self.data)

    def printCheckParameters(self):
        print(f'Chunk {self.type} ')
        print(f"Length: {self.length}")
        print(f'Crc: {self.crc}')
        print(f'Row data: {self.data}')


