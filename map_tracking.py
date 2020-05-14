



from ui_videoframe import CropArea



class MapProperty(tuple):
    def __new__(self, name: str, maskFileLoc: str, startLocaion: CropArea, endLocation: CropArea):
        MapProperty.name = property(operator.itemgetter(0))
        MapProperty.maskFileLoc = property(operator.itemgetter(1))
        MapProperty.startLocaion = property(operator.itemgetter(2))
        MapProperty.endLocation = property(operator.itemgetter(3))

        return tuple.__new__(MapProperty, (name, maskFileLoc, startLocaion, endLocation ))





class Map:

    def __init__(self, map: MapProperty):
        self.map = map


    def getStartPosition(frame):
        crop = self.map.startLocaion
        crop_frame = frame[crop.area.y:crop.area.ys, crop.area.x:crop.area.xs]
        low_txt = pytesseract.image_to_string(crop_frame, lang='eng').lower()
        if crop.requiredMatch and (low_txt not in crop.expectedStrs):
            return False
        return True


    def getCurrentPosition(frame):
