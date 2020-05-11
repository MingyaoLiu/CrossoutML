
import crossml_pb2

class Settings(object):


    def __init__(self):
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


    def saveSettings(self):
        settingsFile = open("settings.bin", "wb")
        settingsFile.write(self.settings.SerializeToString())
        settingsFile.close()


global_settings = None


def getGlobalSetting():
    global global_settings
    if global_settings:
        return global_settings
    else:
        global_settings = Settings()
        return global_settings