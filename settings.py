from simple_log import log

class SettingHandler:
    settings = {"show_hidden_files":"False"}
    filename = "settings.txt"
    guipy_location = None

    def __init__(self, basepath):
        self.guipy_location = basepath
        self.filename = self.guipy_location + "/" + self.filename

    def save_settings(self):
        try:
            log("Saving settings.", "i")
            with open(self.filename, "w") as settings_file:
                for key in self.settings:
                    settings_file.write(f"{key}:{self.settings[key]}")
        except:
            log("Unable to save settings.", "e")

    def load_settings(self):
        try:
            log("Loading settings.", "i")
            with open(self.filename, "r") as settings_file:
                for line in settings_file:
                    _line = line.split(":")
                    self.settings[_line[0]] = _line[1]
        except:
            log("Setting file not found. Generating a default settings file.", "e")
            self.save_settings()
            self.load_settings()

    def change_setting(self, setting, value):
        self.settings[setting] = value
        self.save_settings()