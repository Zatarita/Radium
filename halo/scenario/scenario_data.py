"""
        Scenario Data
            last edited 04/03/2020
"""
from PyQt5.QtCore import QFileInfo

from reclaimer.halo_script.hsc import hsc_bytecode_to_string, get_hsc_data_block
from reclaimer.hek.defs.scnr import scnr_def, halo_script
from reclaimer.misc.defs.ra_test_def import r_a_stream_v0_def, r_a_stream_v3_def, r_a_stream_v4_def


class ScenarioData():
    scenario_path = ""
    scenario_name = ""
    scripts = {}
    globals = []
    recorded_animations = {}

    data = None

    def __init__(self, file_path):
        self.scenario_path = file_path
        self.scenario_name = QFileInfo(file_path).baseName()
        self.data = scnr_def.build(filepath=file_path).data.tagdata
        return

    def parse_scripts(self):
        syntax = get_hsc_data_block(self.data.script_syntax_data.data)
        for i in range(len(self.data.scripts.scripts_array) - 1):
            script_data = hsc_bytecode_to_string(syntax, self.data.script_string_data.data.decode("latin-1"), i, self.data.scripts.STEPTREE, self.data.globals.STEPTREE, "script")
            self.scripts.update({self.data.scripts.scripts_array[i].name : script_data})
        return

    def parse_globals(self):
        syntax = get_hsc_data_block(self.data.script_syntax_data.data)
        for i in range(len(self.data.globals.globals_array) - 1):
            self.globals.append(hsc_bytecode_to_string(syntax, self.data.script_string_data.data.decode("latin-1"), i, self.data.scripts.STEPTREE, self.data.globals.STEPTREE, "global"))

    def parse_recorded_animations(self):
        for RA in self.data.recorded_animations.recorded_animations_array:
            if RA.unit_control_data_version == 4:
                self.recorded_animations.update({RA.name : r_a_stream_v4_def.build(rawdata=RA.recorded_animation_event_stream.data)})
            if RA.unit_control_data_version == 3:
                self.recorded_animations.update({RA.name : r_a_stream_v3_def.build(rawdata=RA.recorded_animation_event_stream.data)})
            if RA.unit_control_data_version == 0:
                self.recorded_animations.update({RA.name : r_a_stream_v0_def.build(rawdata=RA.recorded_animation_event_stream.data)})
            return

    def parse_scenario_data(self):
        self.parse_scripts()
        self.parse_globals()
        self.parse_recorded_animations()

    def save_scripts(self, path):
        for name, data in self.scripts.items():
            try: os.mkdir(path)
            except: pass
            with open(path + name + ".hsc", "w") as file:
                file.write(data)

    def save_globals(self, path):
        try: os.mkdir(path)
        except: pass
        with open(path + self.scenario_name + ".hsc", "w") as file:
            for Global in self.globals:
                file.write(Global + "\n")
