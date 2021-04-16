class PLTE:
    def __init__(self, data):
        self.data = data
        self.palette = []
        self.getPalette()

    def printRowData(self):
        print(self.data)

    def getPalette(self):
        for bytesIndex in range(0,len(self.data),3):
            pixel = self.data[bytesIndex:bytesIndex+3]
            pixelPalette = (pixel[0],pixel[1],pixel[2])
            self.palette.append(pixelPalette)
