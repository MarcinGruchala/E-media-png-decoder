'''
File with EncoderDecoder class
'''
import zlib
import struct
from key import Key
from rsa import Rsa
from Png import Png

class EncoderDecoder():
    '''
    Class saves encrypted and decrypted image data into new files.
    '''
    def __init__(self,png_image,key_size_in_bytes):
        self.key = Key(key_size_in_bytes)
        self.encrypted_data = Rsa.ecb_encrypt(png_image.IDATDecoder.decompressedData, self.key.public)
        self.decryptted_data = Rsa.ecb_decrypt(self.encrypted_data, self.key.private)

    def encrypt_file(self,png_image):
        '''
        Method saves encrypted image data into encrypted.png
        '''
        file_name = "encrypted.png"
        new_file = open(file_name, 'wb')
        new_file.write(Png.PNG_SIGNATURE)
        for chunk in png_image.chunks:
            if chunk.type == b'IDAT':
                idat_data = bytes(self.encrypted_data)
                new_data = zlib.compress(idat_data,9)
                new_crc= zlib.crc32(new_data, zlib.crc32(struct.pack('>4s', b'IDAT')))
                new_length = len(new_data)
                new_file.write(struct.pack('>I',new_length))
                new_file.write(chunk.type)
                new_file.write(new_data)
                new_file.write(struct.pack('>I',new_crc))
            else:
                new_file.write(struct.pack('>I',chunk.length))
                new_file.write(chunk.type)
                new_file.write(chunk.data)
                new_file.write(struct.pack('>I',chunk.crc))
        new_file.close()

    def decrypt_file(self, png_image):
        '''
        Method saves decrypted image data into decrypted.png
        '''
        file_name = "decrypted.png"
        new_file = open(file_name, 'wb')
        new_file.write(Png.PNG_SIGNATURE)
        for chunk in png_image.chunks:
            if chunk.type == b'IDAT':
                idat_data = bytes(self.decryptted_data)
                new_data = zlib.compress(idat_data,9)
                new_crc= zlib.crc32(new_data, zlib.crc32(struct.pack('>4s', b'IDAT')))
                new_length = len(new_data)
                new_file.write(struct.pack('>I',new_length))
                new_file.write(chunk.type)
                new_file.write(new_data)
                new_file.write(struct.pack('>I',new_crc))
            else:
                new_file.write(struct.pack('>I',chunk.length))
                new_file.write(chunk.type)
                new_file.write(chunk.data)
                new_file.write(struct.pack('>I',chunk.crc))
        new_file.close()
