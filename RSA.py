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
            raw_data = bytes(png_data[i:i+step])
            message = int.from_bytes(raw_data, 'big')
            encrypted_message = pow(message, key[0], key[1])
            encrypted_data = encrypted_message.to_bytes(step+1, 'big')
            for byte in encrypted_data:
                encrypted_image_data.append(byte)
        return encrypted_image_data

    @staticmethod
    def ecb_decrypt(png_data,key):
        '''
        Method decrypts image data using ECB
        '''
        key_size = key[1].bit_length()
        decrypted_image_data = []
        step = key_size//8

        for i in range(0, len(png_data), step):

            encrypted_data = b''
            for byte in png_data[i:i+step]:
                encrypted_data += byte.to_bytes(1, 'big')

            encrypted_message = int.from_bytes(encrypted_data, 'big')
            decrypted_message = pow(encrypted_message, key[0], key[1])
            decrypted_data = decrypted_message.to_bytes(step-1, 'big')
            for decrypted_byte in decrypted_data:
                decrypted_image_data.append(decrypted_byte)
        return decrypted_image_data
