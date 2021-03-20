import sys 
import cv2 as cv
import png 

class Decoder:
    def __init__(self, filePath):
        self.img = png.Reader(filePath)
        self.width = None
        self.height = None
        self.bitDepth = None
        self.colorType = None
        self.compressionMethod = None
        self.interlaceMethod = None

    def getColorType(self,metadata):
        colorType = '' 
        if(metadata['greyscale']):
            colorType += 'greyscala'
        else:
            colorType += 'RGB'
        if(metadata['alpha']):
            colorType += ' + alpha sample'
        return colorType


        
        
    def IHDRChunk(self):
        data = self.img.read()
        print(data)
        self.width = data[0]
        self.height = data[1]
        self.bitDepth = data[3]['bitdepth']
        self.colorType = self.getColorType(data[3])
        self.interlaceMethod = data[3]['interlace']
        

    def printData(self):
        print(f'IHDR Chunk:\n   Width: {self.width}\n   Height: {self.height}\n   Bit Depth: {self.bitDepth}\n   Color type: {self.colorType}')
        print(f'   Interlace: {self.interlaceMethod}')



def main():
    png = Decoder(sys.argv[1])
    png.IHDRChunk()
    # png.printData()
    print(png.img.chunk())



if __name__ == '__main__':
    main()

    