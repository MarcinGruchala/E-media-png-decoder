import sys 
import cv2 as cv

def main():
    img = cv.imread(sys.argv[1])
    cv.imshow('PNG image', img)
    cv.waitKey(0)

if __name__ == '__main__':
    main()

    