from os.path import expanduser
from halo.scenario.scenario_data import ScenarioData

class RadiumProject:
    project_name = "Radium Project"                 #Project name
    project_directory = expanduser("~") + "/Radium" #Project directory
    halo_directory = ""                             #Halo directory
    scenario_data = []                              #Scenario data loaded with reclaimer

    backup_count = 0                                #How many backups should we save
    backup_duration = -1                            #How long between backups

    auto_save_duration = 0                          #How long between autosaves?
    auto_save_only_current_document = False         #Only save the document focused.

    script_consolidation = True                     #Condense all scripts into one file at compile
    integrity_check = True                          #Verify script syntax at compile
    resolve_tag_reference = True                    #Find tag data in the map, and use it in script
    resolve_external_tag_references = False         #Find tag data not in map, and use it in script
    multiplayer_desync_checker = False              #Throw warnings for functions that cause desync
    advanced_math_functions = False                 #sin, cos, tan, ect...
    save_decompiled_scripts = True                  #Save a local copy of scripts and globals (faster)

    script_directory = ""                           #local script directory
    recorded_animation_directory = ""               #local recorded animation directory
    backup_directory = "NA"                         #backup directory

    def __init__(self):
        return

    def load_project(self, file_name):
        self.scenario_data.clear()
        if file_name == '':
            return False
        with open(file_name, "r") as file_load:
            self.project_name = str(file_load.readline()).rstrip('\n')
            self.project_directory = str(file_load.readline()).rstrip('\n')
            self.script_directory = str(file_load.readline()).rstrip('\n')
            self.recorded_animation_directory = str(file_load.readline()).rstrip('\n')
            self.backup_directory = str(file_load.readline()).rstrip('\n')

            for line in file_load:
                self.scenario_data.append(ScenarioData(str(line).rstrip('\n')))
        return True

    def save_project(self, file_path):
        if file_path == "":
            return False
        with open(file_path, "w") as save_file:
            save_file.write(self.project_name + "\n")
            save_file.write(self.project_directory + "\n")
            save_file.write(self.script_directory + "\n")
            save_file.write(self.recorded_animation_directory + "\n")
            save_file.write(self.backup_directory + "\n")
            for scenario in self.scenario_data:
                save_file.write(scenario.scenario_path)
                save_file.write("\n")
        return True

    def load_scenario_data(self):
        if not self.scenario_data:
            return
        for scenario in self.scenario_data:
            scenario.parse_scenario_data()

    def backup_project(self):
        pass
        #copy the project contents into designated backup folder
