import sys
import cv2
from PIL import Image
from Decoder import Decoder

def main():

    try:
        imageFile = open(sys.argv[1], 'rb')
    except FileNotFoundError:
        print("File not found")
        return

    if(imageFile.read(len(Decoder.PNG_SIGNATURE)) != Decoder.PNG_SIGNATURE):
        print('Is is not a png file ')
    else:
        cvImg = cv2.imread(sys.argv[1],cv2.IMREAD_GRAYSCALE)
        png = Decoder(imageFile,cvImg)
        png.showMetedata()
        png.showImg()
        if(sys.argv.__len__() == 3):
            if(sys.argv[2] == 'FFT'):
                png.showFFT()
            if(sys.argv[2] == 'PIXELS'):
                png.showPixelData()
            if(sys.argv[2] == 'NI'):
                png.createImageFromCriticalChunks()
            if(sys.argv[2] == 'PLTE'):
                if(png.PLTE.length == 0):
                    print("That image don't have PLTE chunk")
                else:
                    png.showPLTEPalette()

if __name__ == '__main__':
    main()

