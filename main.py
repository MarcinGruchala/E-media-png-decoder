import sys
import cv2
from Decoder import Decoder

def main():
    imageFile = open(sys.argv[1], 'rb')
    if(imageFile.read(len(Decoder.PNG_SIGNATURE)) != Decoder.PNG_SIGNATURE):
        print('Is is not a png file ')
    else:
        cvImg = cv2.imread(sys.argv[1],cv2.IMREAD_GRAYSCALE)

        png = Decoder(imageFile,cvImg)
        # png.printChunks()
        png.printMetedata()
        png.showPixelData()


        # png.readIHDR()
        # png.printMetedata()
        # png.readIDAT()
        # png.showIDAT()
        # png.showFFT()


if __name__ == '__main__':
    main()

