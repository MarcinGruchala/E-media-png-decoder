import sys
from Decoder import Decoder

def main():
    imageFile = open(sys.argv[1], 'rb')
    if(imageFile.read(len(Decoder.PNG_SIGNATURE)) != Decoder.PNG_SIGNATURE):
        print('Is is not a png file ')
    else:
        png = Decoder(imageFile)
        png.printChunks()
        png.readIHDR()
        png.ihdr.printNice()

if __name__ == '__main__':
    main()

