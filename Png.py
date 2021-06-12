'''
File with class representing png image
'''
import zlib
import copy
import cv2
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
from IHDR import IHDR, struct
from IDAT import IDAT
from PLTE import PLTE
from Chunk import Chunk
from IDATDecoder import IDATDecoder

class Png:
    '''
    Class representing png image
    '''
    PNG_SIGNATURE = b'\x89PNG\r\n\x1a\n'
    CRITICAL_CHUNKS = [b'IHDR',b'PLTE',b'IDAT',b'IEND']

    def __init__(self, image,cvImg):
        self.img = image
        self.cvImg = cvImg
        self.chunks = self.read_chunks()
        self.IHDR = self.read_IHDR()
        self.bytes_per_pixel = self.get_bytes_per_pixel()
        self.PLTE = self.read_PLTE()
        self.IDATs = self.read_IDATs()
        self.IDATDecoder = IDATDecoder(
            self.IDATs,
            self.IHDR.width,
            self.IHDR.height,
            self.bytes_per_pixel
            )

    def read_chunk(self,file):
        '''
        Method reads data from chunk
        '''
        chunk_length, chunk_type = struct.unpack(
            '>I4s',
            file.read(Chunk.LENGTH_BYTES+Chunk.TYPE_BYTES)
            )
        chunk_data = file.read(chunk_length)
        check_sum = zlib.crc32(chunk_data, zlib.crc32(struct.pack('>4s', chunk_type)))
        chunk_crc, = struct.unpack('>I', file.read(Chunk.CRC_BYTES))
        if chunk_crc != check_sum:
            raise Exception('chunk checksum failed {} != {}'.format(chunk_crc,
                check_sum))
        return Chunk(chunk_length,chunk_type,chunk_data,chunk_crc)

    def read_chunks(self):
        '''
        Method reads image chunks
        '''
        chunks = []
        while True:
            chunk = self.read_chunk(self.img)
            chunks.append(chunk)
            if chunk.type == b'IEND':
                break
        return chunks

    def read_IHDR(self):
        '''
        Method reads IHDR chunk
        '''
        return IHDR(self.chunks[0])

    def read_PLTE(self):
        '''
        Method reads PLTE chunk
        '''
        for chunk in self.chunks:
            if chunk.type == b'PLTE' :
                return PLTE(chunk.length,chunk.type,chunk.data,chunk.crc)
        return PLTE(0,b'PLTE',b'',0)

    def read_IDATs(self):
        '''
        Method returns all IDAT chunks
        '''
        return [IDAT(chunk) for chunk in self.chunks if chunk.type == b'IDAT']

    def get_bytes_per_pixel(self):
        '''
        Method returns bytes per pixel
        '''
        if self.IHDR.colorType == 0 :
            return 1
        if self.IHDR.colorType == 2 :
            return 3
        if self.IHDR.colorType == 3 :
            return 1
        if self.IHDR.colorType == 4 :
            return 2
        if self.IHDR.colorType == 6 :
            return 4
        return -1

    def print_chunks(self):
        '''
        Method prints image chunks
        '''
        print([chunk.type for chunk in self.chunks])

    def show_img(self):
        '''
        Method shows image using PIL library
        '''
        Image.open(self.img).show()

    def print_image_informations(self):
        '''
        Method prints basic image information in the console
        '''
        print("Chunks: ")
        self.print_chunks()
        print("\nImage atributes: ")
        self.IHDR.printInformations()
        print(f'Bytes per pixel: {self.bytes_per_pixel}')

    def show_fft(self):
        '''
        FFT method - needs correction
        '''
        befor_fft = self.cvImg
        fft = np.fft.fft2(self.cvImg)
        fft_centered = np.fft.fftshift(fft)
        fft_decentered = np.fft.ifftshift(fft_centered)
        invert_fft = np.fft.ifft2(fft_decentered)
        plt.subplot(221)
        plt.imshow(befor_fft, 'gray')
        plt.title("Orgiinal Image in grayscale")
        plt.subplot(222)
        plt.imshow(np.log(1+np.abs(fft)), "gray")
        plt.title("Spectrum")
        plt.subplot(223)
        plt.imshow(np.log(1+np.abs(fft_centered)), "gray")
        plt.title("Centered Spectrum")
        plt.subplot(224)
        plt.imshow(np.abs(invert_fft), "gray")
        plt.title("Image after inverse FFT")
        plt.show()

    def show_pixel_data(self):
        '''
        Method shows pixes data from IDAT chunks
        '''
        plt.imshow(np.array(self.IDATDecoder.reconstructedPixelData).reshape((self.IHDR.height, self.IHDR.width, self.bytes_per_pixel)))
        plt.show()

    def show_PLTE_palette(self):
        '''
        Method shows PLTE colour palette
        '''
        palette_graf = np.array(self.PLTE.palette)
        i = np.arange(256).reshape(16,16)
        plt.imshow(palette_graf[i])
        plt.show()

    def create_image_from_critical_chunks(self):
        '''
        Method creates new png file from critical chunks
        '''
        file_name = "newPNGImage.png"
        new_file = open(file_name, 'wb')
        new_file.write(Png.PNG_SIGNATURE)
        for chunk in self.chunks:
            if chunk.type in Png.CRITICAL_CHUNKS:
                new_file.write(struct.pack('>I',chunk.length))
                new_file.write(chunk.type)
                new_file.write(chunk.data)
                new_file.write(struct.pack('>I',chunk.crc))
        new_file.close()
