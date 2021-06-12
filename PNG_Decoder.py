'''
File with app menu app logic
'''
import sys
import cv2
from encoder_decoder import EncoderDecoder
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
    if flag == '-fft':
        png.show_fft()
    elif flag == '-show':
        png.show_img()
    elif flag == '-id':
        png.show_pixel_data()
    elif flag == '-ni':
        png.create_image_from_critical_chunks()
    elif flag == '-p':
        if png.PLTE.length == 0:
            print("\nThat image doesn't have PLTE chunk")
        else:
            png.show_PLTE_palette()
    elif flag == '-RSA':
        encoder_decoder = EncoderDecoder(png, int(sys.argv[3]))
        encoder_decoder.encrypt_file(png)
        encoder_decoder.decrypt_file(png)
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
                png.print_image_informations()

                if sys.argv.__len__() > 2:
                    flag_action(png,sys.argv[2])

if __name__ == '__main__':
    menu()
