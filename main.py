import sys
import struct
import zlib

class Decoder:
    PNG_SIGNATURE = b'\x89PNG\r\n\x1a\n'
    # def __init__(self, filePath):
    #     self.img = png.Reader(filePath)


def read_chunk(file):
    chunkLength, chunkType = struct.unpack('>I4s', file.read(8))
    chunkData = file.read(chunkLength)
    checksum = zlib.crc32(chunkData, zlib.crc32(struct.pack('>4s', chunkType)))
    chunk_crc, = struct.unpack('>I', file.read(4))
    if chunk_crc != checksum:
        raise Exception('chunk checksum failed {} != {}'.format(chunk_crc,
            checksum))
    return chunkType, chunkData



def main():
    imageFile = open(sys.argv[1], 'rb')
    if(imageFile.read(len(Decoder.PNG_SIGNATURE)) != Decoder.PNG_SIGNATURE):
        print('Is is not a png file ')
    else:
        chunks = []
        while True:
            chunkType, chunkData = read_chunk(imageFile)
            chunks.append((chunkType, chunkData))
            if chunkType == b'IEND':
                break

        print([chunkType for chunkType, chunkData in chunks])

        IHDR = chunks[0][1]
        width, height, bitDepth, colorType, compressionMethod, filterMethod, interlaceMethod = struct.unpack('>IIBBBBB', IHDR)

        print(f'\n{chunks[0][0]}')
        print(f'Width: {width}\nHeight: {height}\nBit Depth: {bitDepth}\nColor type: {colorType}')
        print(f'Compression Method: {compressionMethod}\nFilter Method: {filterMethod}')
        print(f'Interlace Method: {interlaceMethod}')




if __name__ == '__main__':
    main()

