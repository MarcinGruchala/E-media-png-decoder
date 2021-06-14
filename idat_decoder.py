'''
File with class IdatDecoder
'''
import zlib
class IDATDecoder():
    '''
    Class decodes IDATs chunks
    '''
    def __init__(self ,IDATs, width, height, bytes_per_pixel):
        self.width = width
        self.height = height
        self.bytes_per_pixel =bytes_per_pixel
        self.IDATs_data = b''.join(chunk.data for chunk in IDATs)
        self.decompressed_data = zlib.decompress(self.IDATs_data)
        self.stride = width * bytes_per_pixel
        self.reconstructed_pixel_data = []
        self.reconstructs_pixel_data()

    def paeth_predictor(self,a, b, c):
        '''
        TO DO
        '''
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

    def reconstructed_pixel_data_a(self, r, c):
        '''
        TO DO
        '''
        return self.reconstructed_pixel_data[r * self.stride + c - self.bytes_per_pixel] if c >= self.bytes_per_pixel else 0

    def reconstructed_pixel_data_b(self, r, c):
        '''
        TO DO
        '''
        return self.reconstructed_pixel_data[(r-1) * self.stride + c] if r > 0 else 0

    def reconstructed_pixel_data_c(self, r, c):
        '''
        TO DO
        '''
        return self.reconstructed_pixel_data[(r-1) * self.stride + c - self.bytes_per_pixel] if r > 0 and c >= self.bytes_per_pixel else 0

    def reconstructs_pixel_data(self):
        '''
        TO DO
        '''
        i = 0
        for r in range(self.height):
            filter_type = self.decompressed_data[i]
            i += 1
            for c in range(self.stride):
                filtr_x = self.decompressed_data[i]
                i += 1
                if filter_type == 0:
                    reconstructed_pixel_data_x = filtr_x
                elif filter_type == 1:
                    reconstructed_pixel_data_x = filtr_x + self.reconstructed_pixel_data_a(r, c)
                elif filter_type == 2:
                    reconstructed_pixel_data_x = filtr_x + self.reconstructed_pixel_data_b(r, c)
                elif filter_type == 3:
                    reconstructed_pixel_data_x = filtr_x + (self.reconstructed_pixel_data_a(r, c) + self.reconstructed_pixel_data_b(r, c)) // 2
                elif filter_type == 4:
                    predicted_peath = self.paeth_predictor(
                        self.reconstructed_pixel_data_a(r, c),
                        self.reconstructed_pixel_data_b(r, c),
                        self.reconstructed_pixel_data_c(r, c)
                        )
                    reconstructed_pixel_data_x = filtr_x + predicted_peath
                else:
                    raise Exception('unknown filter type: ' + str(filter_type))
                self.reconstructed_pixel_data.append(reconstructed_pixel_data_x & 0xff)
