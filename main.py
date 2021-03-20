import sys 
import cv2 as cv

class Decoder:
    def __init__(self, filePath):
        self.img = cv.imread(filePath, cv.IMREAD_COLOR)
        self.imgWidth = 0
        self.imgHeight = 0
        
    def IHDRChunk(self):
        self.imgHeight, self.imgWidth = self.img.shape[:2]

    def printData(self):
        cv.imshow('PNG image', self.img)
        print(self.img.shape)
        print("Width: ", self.imgWidth)
        print("Height: ", self.imgHeight)
    pass



def main():
    decoder = Decoder(sys.argv[1])
    decoder.IHDRChunk()
    decoder.printData()
    cv.waitKey(0)

if __name__ == '__main__':
    main()

    