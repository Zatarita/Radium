from PyQt5.QtWidgets import QFileDialog
from PyQt5.QtCore import QFileInfo

from UI.logic.new_item.new_item import NewItemDialog
from halo.scenario.scenario_data import ScenarioData

import os
class Menu():
    def __init__(self):
        pass

    def new(self, project, settings):
        #create a new project dialog, and show the window
        new_project_window = NewItemDialog()
        if not new_project_window.exec_():
            return

        #Collect Project Information from new project window
        project.project_name = new_project_window.ProjectName.text()
        project.project_directory = new_project_window.ProjectDirectory.text()
        project.script_directory = new_project_window.ScriptsDirectory.text()
        project.recorded_animation_directory = new_project_window.RecordedAnimationsDirectory.text()

        project.BackupDirectory = new_project_window.BackupDirectory.text()
        project.BackupCount = new_project_window.new_project_advanced.BackupCount.value()
        project.BackupDuration = new_project_window.new_project_advanced.BackupTime.value()

        project.AutoSaveDuration = new_project_window.new_project_advanced.TimeBetweenSaves.value()
        project.AutoSaveOnlyCurrentDocument = new_project_window.new_project_advanced.SaveOnlyCurrent.isChecked()

        #ScriptConsolidation, IntegrityCheck, ResolveTagReferences, ResolveExternalTagReferences
        #MultiplayerDesycChecker, AdvancedMathFunctions
        #Create Directories and Files
        if(project.project_directory == ""):
            project.project_directory = settings.default_project_directory+project.project_name
        if not os.path.exists(project.project_directory):
            os.mkdir(project.project_directory)

        if new_project_window.EnableLocalScriptDirectory.isChecked() == True:
            if project.script_directory == "":
                project.script_directory = project.project_directory+"/Scripts"
            if not os.path.exists(project.script_directory):
                os.mkdir(project.script_directory)

        if new_project_window.EnableLocalRecordedAnimationDirectory.isChecked() == True:
            if project.recorded_animation_directory == "":
                project.recorded_animation_directory = project.project_directory+"/Recorded Animations"
            if not os.path.exists(project.recorded_animation_directory):
                os.mkdir(project.recorded_animation_directory)

        if new_project_window.EnableBackup.isChecked() == True:
            if project.BackupDirectory == "":
                project.backup_directory = project.project_directory+"/Backup"
            if not os.path.exists(project.BackupDirectory):
                os.mkdir(project.BackupDirectory)

        project.scenario_data.clear()

        for index in range(new_project_window.bind_scenarios.ScenarioList.count()):
            project.scenario_data.append(ScenarioData(new_project_window.bind_scenarios.ScenarioList.item(index).text()))

        #Save Project
        project.save_project(project.project_directory+"/"+project.project_name+".ra")

        #Parse scenario data
        project.load_scenario_data()
        #if project.save_decompiled_scripts:
            #for scenario in project.scenario_data:
                #scenario.save_scripts(project.script_directory + "/" + scenario.scenario_name + "/")
                #scenario.save_globals(project.script_directory + "/" + scenario.Scenscenario_name + "/globals/")

        self.project_file_browser.setRootPath(project.project_directory)
        Index = self.project_file_browser.index(project.project_directory)
        self.ProjectContents.setRootIndex(Index)
        self.UpdateUI()
        return

    def Open(self):
        file_name, _ = QFileDialog.getOpenFileName(None, "Open Project", "", "All (*.*);;All Known (*.def *.hsc *.scenario.recorded_animation *.ra);;Syntax Definition (*.def);;Halo Script (*.hsc);;Recorded Animation (*.scenario.recorded_animation);;Radium Project (*.ra)")
        file_info = QFileInfo(file_name)

        if file_info.completeSuffix()=="ra":
            self.OpenProject(None, file_name)
            return

        with open(file_name, "r") as file:
            content = file.read()

        extension_handler = {
        "def"                          : TextTab(file_info.fileName(), file_name, content, "def"),
        "acd"                          : TextTab(file_info.fileName(), file_name, content, "acd"),
        "hsc"                          : TextTab(file_info.fileName(), file_name, content, "hsc"),
        ".scenario.recorded_animation" : None #openGL tab
        }
        tab = extension_handler.get(file_info.completeSuffix(), None)
        if tab:
            tab.AddTab(self.TabCanvas)
        return

    def OpenProject(self, file = ""):
        if file == "":
            file_name, _ = QFileDialog.getOpenFileName(self,"Open Project", self.settings.default_project_directory , "Radium Project (*.ra)")
            if file_name == "":
                return
        else:
            file_name = file

        self.TextOut.append("Loading Project: " + file_name)
        self.project.load_project(file_name)
        self.project_file_browser.setRootPath(self.project.project_directory)
        index = self.project_file_browser.index(self.project.project_directory)
        self.ProjectContents.setRootIndex(index)

        self.TextOut.append("Loading scenario(s)")
        self.ParseScenarioData()
        self.UpdateUI()
        return

    def Save(self):
        if type(self.TabCanvas.widget(self.TabCanvas.currentIndex())) != QWidget:
            if self.TabCanvas.widget(self.TabCanvas.currentIndex()).Path == "":
                file, _ = QFileDialog.getSaveFileName(self, 'Save File')
                File = QFileInfo(file)
                if File.fileName() == "":
                    return
                self.TabCanvas.widget(self.TabCanvas.currentIndex()).Path = File.absoluteFilePath()
                self.TabCanvas.widget(self.TabCanvas.currentIndex()).Title = File.fileName()
                self.TabCanvas.setTabText(self.TabCanvas.currentIndex(), File.fileName())
            self.TextOut.append("Saving: " + self.TabCanvas.widget(self.TabCanvas.currentIndex()).Title)
            self.TabCanvas.widget(self.TabCanvas.currentIndex()).Save()
            self.TabCanvas.widget(self.TabCanvas.currentIndex()).isDirty = False
        return

    def Update(self):
        url = 'https://raw.githubusercontent.com/Zatarita/Radium/master/_BUILD'
        Version = requests.get(url, allow_redirects=False).text
        Major, Minor, Patch = Version.split(".")
        UpdateNeeded = False
        if int(Major) > self.Settings.RadiumVersion[0]:
            UpdateNeeded = True
        elif int(Major) == self.Settings.RadiumVersion[0]:
            if int(Minor) > self.Settings.RadiumVersion[1]:
                UpdateNeeded = True
            elif int(Minor) == self.Settings.RadiumVersion[1]:
                if int(Patch) > self.Settings.RadiumVersion[2]:
                    UpdateNeeded = True
        if UpdateNeeded:
            self.TextOut.append("Update available: v" + Version)
            #UpdateHandler.Update()
        return

    def SaveAll(self, parent = None):
        for i in range(self.TabCanvas.count()):
            if type(self.TabCanvas.widget(i)) != QWidget:
                self.TabCanvas.widget(i).Save()
        return

    def SaveAs(self, parent = None):
        file, _ = QFileDialog.getSaveFileName(self, 'Save Project')
        File = QFileInfo(file)
        if File.fileName() == "":
            return
        if type(self.TabCanvas.widget(self.TabCanvas.currentIndex())) != QWidget:
            self.TextOut.append("Saving: " + self.TabCanvas.widget(self.TabCanvas.currentIndex()).Title + " as " + File.absoluteFilePath())
            self.TabCanvas.widget(self.TabCanvas.currentIndex()).Title = File.fileName()
            self.TabCanvas.widget(self.TabCanvas.currentIndex()).Path = File.absoluteFilePath()
            self.TabCanvas.setTabText(self.TabCanvas.currentIndex(), File.fileName())
            self.TabCanvas.widget(self.TabCanvas.currentIndex()).Save()
            self.TabCanvas.widget(self.TabCanvas.currentIndex()).isDirty = False
        return
        return

    def Quit(self):
        QApplication.quit()
        return

    def Undo(self):
        self.AssignStyleSheet()
        return

    def Redo(self):
        return

    def Cut(self):
        return

    def Copy(self):
        return

    def Paste(self):
        return

    def BuildScripts(self):
        return

    def BuildHaloCache(self):
        return

    def ScriptCompileAndBuild(self):
        return

    def ImportRecordedAnimation(self):
        return

    def ImportScript(self):
        return

    def BindScenario(self):
        return

    def ShowProjectSettings(self):
        self.ProjectSettingsWindow.exec_()
        return

    def RemoveBoundScenario(self):
        return

    def ShowHelp(self):
        return

    def ShowAbout(self):
        return

    def SubmitABug(self):
        return

    def NewRecordedAnimation(self):
        return

    def NewScript(self):
        return
