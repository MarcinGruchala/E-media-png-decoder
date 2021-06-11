from Key import Key

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
    def Ecb_decrypt(self, pngData):
        pass