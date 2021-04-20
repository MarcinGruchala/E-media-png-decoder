import zlib
class IDATDecoder():
    def __init__(self ,IDATs, width, height, bytesPerPixel):
        self.width = width
        self.height = height
        self.bytesPerPixel =bytesPerPixel
        self.IDATsData = b''.join(chunk.data for chunk in IDATs)
        self.decompressedData = zlib.decompress(self.IDATsData)
        self.stride = width * bytesPerPixel
        self.reconstructedPixelData = []
        self.reconstructsPixelData()

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
        for r in range(self.height):
            filter_type = self.decompressedData[i]
            i += 1
            for c in range(self.stride):
                Filt_x = self.decompressedData[i]
                i += 1
                if filter_type == 0:
                    reconstructedPixelData_x = Filt_x
                elif filter_type == 1:
                    reconstructedPixelData_x = Filt_x + self.reconstructedPixelData_a(r, c)
                elif filter_type == 2:
                    reconstructedPixelData_x = Filt_x + self.reconstructedPixelData_b(r, c)
                elif filter_type == 3:
                    reconstructedPixelData_x = Filt_x + (self.reconstructedPixelData_a(r, c) + self.reconstructedPixelData_b(r, c)) // 2
                elif filter_type == 4:
                    reconstructedPixelData_x = Filt_x + self.paethPredictor(self.reconstructedPixelData_a(r, c), self.reconstructedPixelData_b(r, c), self.reconstructedPixelData_c(r, c))
                else:
                    raise Exception('unknown filter type: ' + str(filter_type))
                self.reconstructedPixelData.append(reconstructedPixelData_x & 0xff)

