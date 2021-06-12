from EncoderDecoder import EncoderDecoder
from Key import Key
from PrimeNumber import PrimeNumber
import sys
import cv2
from Png import Png

def printHelp():
    print("usage: python main.py [file name] [-flag]")
    print("flags:")
    print("-id - IDAT chunk data")
    print("-p - colors palette for images with indexed-color")
    print("-fft - fast fourier transform")
    print("-ni - create new image from critical chunks")

def menu():
    if(sys.argv.__len__() == 1):
        printHelp()
    else:
        if (sys.argv[1] == '-help'):
            printHelp()
        else:
            try:
                imageFile = open(sys.argv[1], 'rb')
            except FileNotFoundError:
                print("File not found")
                return

            if(imageFile.read(len(Png.PNG_SIGNATURE)) != Png.PNG_SIGNATURE):
                print('Is is not a png file ')
            else:
                cvImg = cv2.imread(sys.argv[1],cv2.IMREAD_GRAYSCALE)
                png = Png(imageFile,cvImg)
                png.printImageInformations()
                key = Key()
                if(sys.argv.__len__() == 3):
                    if(sys.argv[2] == '-fft'):
                        png.showFFT()
                    elif(sys.argv[2] == 'show'):
                        png.showImg()
                    elif(sys.argv[2] == '-id'):
                        png.showPixelData()
                    elif(sys.argv[2] == '-ni'):
                        png.createImageFromCriticalChunks()
                    elif(sys.argv[2] == '-p'):
                        if(png.PLTE.length == 0):
                            print("\nThat image doesn't have PLTE chunk")
                        else:
                            png.showPLTEPalette()
                    elif(sys.argv[2] == '-RSA'):
                        encoder_decoder = EncoderDecoder(png)
                        encoder_decoder.encryptFile(png)
                        encoder_decoder.decryptFile(png)                    
                    else:
                        print("Wrong flag")

if __name__ == '__main__':
    menu()
