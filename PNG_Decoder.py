'''
File with app menu app logic
'''
import sys
import cv2
from EncoderDecoder import EncoderDecoder
from Png import Png

def print_help():
    '''
    Function prints flags options
    '''
    print("usage: python main.py [file name] [-flag]")
    print("flags:")
    print("-id - IDAT chunk data")
    print("-p - colors palette for images with indexed-color")
    print("-fft - fast fourier transform")
    print("-ni - create new image from critical chunks")

def flag_action(png,flag):
    '''
    Function handles flag action
    '''
    if sys.argv.__len__() == 3:
        if flag == '-fft':
            png.showFFT()
        elif flag == '-show':
             png.showImg()
        elif flag == '-id':
            png.showPixelData()
        elif flag == '-ni':
            png.createImageFromCriticalChunks()
        elif flag == '-p':
            if png.PLTE.length == 0:
                print("\nThat image doesn't have PLTE chunk")
            else:
                png.showPLTEPalette()
        elif flag == '-RSA':
            encoder_decoder = EncoderDecoder(png)
            encoder_decoder.encryptFile(png)
            encoder_decoder.decryptFile(png)
        else:
            print("Wrong flag")

def menu():
    '''
    Menu logic
    '''
    if sys.argv.__len__() == 1 :
        print_help()
    else:
        if sys.argv[1] == '-help':
            print_help()
        else:
            try:
                image_file = open(sys.argv[1], 'rb')
            except FileNotFoundError:
                print("File not found")
                return

            if image_file.read(len(Png.PNG_SIGNATURE)) != Png.PNG_SIGNATURE:
                print('Is is not a png file ')
            else:
                cv_img = cv2.imread(sys.argv[1],cv2.IMREAD_GRAYSCALE)
                png = Png(image_file,cv_img)
                png.printImageInformations()

                if sys.argv.__len__() == 3:
                    flag_action(png,sys.argv[2])

if __name__ == '__main__':
    menu()
