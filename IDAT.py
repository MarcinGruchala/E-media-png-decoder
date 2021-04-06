import zlib
import matplotlib.pyplot as plt
import numpy as np
class IDAT:
    def __init__(self, idatData):
        self.decompressedData = zlib.decompress(idatData)


