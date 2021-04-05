import zlib
import matplotlib.pyplot as plt
import numpy as np
class IDAT:
    def __init__(self, idatData,bytesPerPixel,width,height):
        self.decompressedData = zlib.decompress(idatData)
        self.reconstructedPixelData = []
        self.bytesPerPixel = bytesPerPixel
        self.width = width
        self.height = height
        self.stride = width * self.bytesPerPixel

    def paethPredictor(self,a, b, c):
        p = a + b - c
        pa = abs(p - a)
        pb = abs(p - b)
        pc = abs(p - c)
        if pa <= pb and pa <= pc:
            Pr = a
        elif pb <= pc:
            Pr = b
        else:
            Pr = c
        return Pr

    def reconstructedPixelData_a(self, r, c):
        return self.reconstructedPixelData[r * self.stride + c - self.bytesPerPixel] if c >= self.bytesPerPixel else 0

    def reconstructedPixelData_b(self, r, c):
        return self.reconstructedPixelData[(r-1) * self.stride + c] if r > 0 else 0

    def reconstructedPixelData_c(self, r, c):
        return self.reconstructedPixelData[(r-1) * self.stride + c - self.bytesPerPixel] if r > 0 and c >= self.bytesPerPixel else 0

    def reconstructsPixelData(self):
        i = 0
        for r in range(self.height): # for each scanline
            filter_type = self.decompressedData[i] # first byte of scanline is filter type
            i += 1
            for c in range(self.stride): # for each byte in scanline
                Filt_x = self.decompressedData[i]
                i += 1
                if filter_type == 0: # None
                    reconstructedPixelData_x = Filt_x
                elif filter_type == 1: # Sub
                    reconstructedPixelData_x = Filt_x + self.reconstructedPixelData_a(r, c)
                elif filter_type == 2: # Up
                    reconstructedPixelData_x = Filt_x + self.reconstructedPixelData_b(r, c)
                elif filter_type == 3: # Average
                    reconstructedPixelData_x = Filt_x + (self.reconstructedPixelData_a(r, c) + self.reconstructedPixelData_b(r, c)) // 2
                elif filter_type == 4: # Paeth
                    reconstructedPixelData_x = Filt_x + self.paethPredictor(self.reconstructedPixelData_a(r, c), self.reconstructedPixelData_b(r, c), self.reconstructedPixelData_c(r, c))
                else:
                    raise Exception('unknown filter type: ' + str(filter_type))
                self.reconstructedPixelData.append(reconstructedPixelData_x & 0xff) # truncation to byte

    def show(self):
        plt.imshow(np.array(self.reconstructedPixelData).reshape((self.height, self.width, self.bytesPerPixel)))
        plt.show()


