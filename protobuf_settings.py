
import crossml_pb2

class Settings(object):


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.settings = crossml_pb2.CrossoutMLSetting()

        with open('settings.bin', 'rb') as f:
            self.settings.ParseFromString(f.read())
            f.close()


    def writeSettings(self, new_setting):

        settingsFile = open("settings.bin", "wb")

        self.settings = new_setting
        print(self.settings)
        settingsFile.write(self.settings.SerializeToString())
        settingsFile.close()
        return 1


    def getSettings(self):
        return self.settings

