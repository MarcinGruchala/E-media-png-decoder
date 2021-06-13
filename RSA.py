'''
File with RSA class
'''
class Rsa():
    '''
    Class encrypts and decrypts image data using ECB
    '''
    @staticmethod
    def ecb_encrypt(png_data,key):
        '''
        Method encrypts image data using ECB
        '''
        key_size = key[1].bit_length()
        encrypted_image_data = []
        step = key_size//8 -1

        for i in range(0, len(png_data), step):
            raw_data_bytes = bytes(png_data[i:i+step])
            raw_data_int = int.from_bytes(raw_data_bytes, 'big')
            encrypted_data_int = pow(raw_data_int, key[0], key[1])
            encrypted_data_bytes = encrypted_data_int.to_bytes(step+1, 'big')
            for encrypted_byte in encrypted_data_bytes:
                encrypted_image_data.append(encrypted_byte)
        return encrypted_image_data
        # key_size =key[1].bit_length()
        # encrypted_data = []
        # padding = []
        # after_iend_data = []
        # step = key_size//8 -1

        # for i in range(0, len(png_data), step):
        #     bytes_block = bytes(png_data[i:i+step])

        #     #padding
        #     if len(bytes_block)%step != 0:
        #         for _ in range(step - (len(bytes_block)%step)):
        #             padding.append(0)
        #         bytes_block = padding + bytes_block

        #     raw_data_int = int.from_bytes(bytes_block, 'big')
        #     encrypt_block_int = pow(raw_data_int, key[0], key[1])
        #     encrypt_block_bytes = encrypt_block_int.to_bytes(step+1, 'big')

        #     after_iend_data.append(encrypt_block_bytes[-1])
        #     encrypt_block_bytes = encrypt_block_bytes[:-1]
        #     encrypted_data += encrypt_block_bytes

        # return encrypted_data, after_iend_data

    @staticmethod
    def ecb_decrypt(png_data,key):
        '''
        Method decrypts image data using ECB
        '''
        key_size = key[1].bit_length()
        decrypted_image_data = []
        step = key_size//8

        for i in range(0, len(png_data), step):
            encrypted_bytes = b''
            for byte in png_data[i:i+step]:
                encrypted_bytes += byte.to_bytes(1, 'big')
            encrypted_data_int = int.from_bytes(encrypted_bytes, 'big')
            decrypted_data_int = pow(encrypted_data_int, key[0], key[1])
            decrypted_data_bytes = decrypted_data_int.to_bytes(step-1, 'big')
            for decrypted_byte in decrypted_data_bytes:
                decrypted_image_data.append(decrypted_byte)
        return decrypted_image_data
