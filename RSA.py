from Key import Key
import numpy as np
class Rsa():

    @staticmethod
    def EcbEncrypt(pngData,key):
        keySize = key[1].bit_length()
        encryptedData = []
        step = keySize//8 -1

        for i in range(0, len(pngData), step):
            raw_data_bytes = bytes(pngData[i:i+step])
            raw_data_int = int.from_bytes(raw_data_bytes, 'big')
            encrypted_data_int = pow(raw_data_int, key[0], key[1])
            encrypted_data_bytes = encrypted_data_int.to_bytes(step+1, 'big')
            for encrypted_byte in encrypted_data_bytes:
                encryptedData.append(encrypted_byte)
        return encryptedData

    @staticmethod
    def EcbDecrypt(pngData,key):
        key_size = key[1].bit_length()
        decrypted_data = []
        step = key_size//8

        for i in range(0, len(pngData), step):
            encrypted_bytes = b''
            for byte in pngData[i:i+step]:
                encrypted_bytes += byte.to_bytes(1, 'big')
            encrypted_data_int = int.from_bytes(encrypted_bytes, 'big')
            decrypted_data_int = pow(encrypted_data_int, key[0], key[1])
            decrypted_data_bytes = decrypted_data_int.to_bytes(step-1, 'big')
            for decrypted_byte in decrypted_data_bytes:
                decrypted_data.append(decrypted_byte)
        return decrypted_data
