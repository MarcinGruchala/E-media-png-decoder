from Key import Key
import zlib
from RSA import Rsa
import struct
from Png import Png

class EncoderDecoder():
    def __init__(self):
        self.key = Key()

    def encryptFile(self,pngImage):
        fileName = "encrypted.png"
        newFile = open(fileName, 'wb')
        newFile.write(Png.PNG_SIGNATURE)
        all_IDAT_Data = Rsa.EcbEncrypt(pngImage.IDATDecoder.IDATsData , self.key.public)
        for chunk in pngImage.chunks:
            if chunk.type == b'IDAT':
                idatData = bytes(all_IDAT_Data)
                newData = zlib.compress(idatData,9)
                newCrc= zlib.crc32(newData, zlib.crc32(struct.pack('>4s', b'IDAT')))
                newLength = len(newData)
                newFile.write(struct.pack('>I',newLength))
                newFile.write(chunk.type)
                newFile.write(newData)
                newFile.write(struct.pack('>I',newCrc))
            else:
                newFile.write(struct.pack('>I',chunk.length))
                newFile.write(chunk.type)
                newFile.write(chunk.data)
                newFile.write(struct.pack('>I',chunk.crc))
        newFile.close()

    def decryptFile(image):
        pass