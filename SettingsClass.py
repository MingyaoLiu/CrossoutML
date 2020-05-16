
import crossml_pb2
from os import path


class Settings(object):

    def __init__(self):
        self.settings = crossml_pb2.CrossoutMLSetting()
        self.getSettingsFile()

    def getSettingsFile(self):
        if path.exists('settings.bin'):
            with open('settings.bin', 'rb') as f:
                self.settings.ParseFromString(f.read())
                f.close()
        else:
            self.settings = crossml_pb2.CrossoutMLSetting()
            self.saveSettings()

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
