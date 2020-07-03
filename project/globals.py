"""
        Radium Globals.
            last edit 07/03/2020

        settings for radium.
"""

from os.path import expanduser

class RadiumGlobals:
    default_project_directory = expanduser("~") + "/Radium/"
    halo_directory = "C:/Program Files (x86)/Microsoft Games/Halo Custom Edition"
    recent_projects = []
    style_sheet = "UI/style_sheets/Default.sts"
    syntax_preferences = {}

    radium_version = [0, 0, 1]

    def __init__(self):
        return

    def save(self):
        try:
            with open("Radium.cfg", "w") as save_file:
                save_file.write(self.default_project_directory + "\n")
                save_file.write(self.halo_directory)
                for Project in self.recent_projects:
                    save_file.write("\n")
                    save_file.write(Project)
            return True
        except: return False

    def load(self):
        if not exists("Radium.cfg"):
            self.save()
            return False

        self.recent_projects.clear()
        file_loader = open("Radium.cfg", "r")
        self.default_project_directory = str(file_loader.readline()).rstrip('\n')
        self.halo_directory = str(file_loader.readline()).rstrip('\n')
        for line in file_loader:
            self.recent_projects.append(str(line).rstrip('\n'))
        return True
