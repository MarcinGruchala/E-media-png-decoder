import zlib
# import matplotlib.pyplot as plt
# import numpy as np
from Chunk import Chunk
class IDAT(Chunk):
    def __init__(self, chunk):
        super().__init__(chunk.length, chunk.type,chunk.data,chunk.crc)



