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
        # png.IHDR.printCheckParameters()
        if(sys.argv.__len__() == 3):
            if(sys.argv[2] == 'FFT'):
                png.showFFT()
            if(sys.argv[2] == 'PIXELS'):
                png.showPixelData()
            if(sys.argv[2] == 'NI'):
                png.createImageFromCriticalChunks()

if __name__ == '__main__':
    main()

