from PyQt5.QtWidgets import *
from PyQt5.QtCore import pyqtSlot as Slot
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5 import uic

import sys, requests, os

from UI.logic.main_window.elements.menu import Menu
from UI.logic.main_window.elements.project_context import ProjectContext
from UI.logic.widgets.tabs.text_tab import TextTab
from project.globals import *
from project.project import *

#from reclaimer.hek.defs.scnr import scnr_def
#from Forms.Widgets.Tabs import *
#from Forms.Project.ProjectSettings import ProjectSettingsDialog

class MainForm(QMainWindow):
    def __init__(self, parent = None):
        QWidget.__init__(self, parent)
        uic.loadUi('UI/design/main_form/main_form.ui', self)
        #Data
        self.project_file_browser = QFileSystemModel()
        self.project = RadiumProject()
        self.settings = RadiumGlobals()

        self.project_browser_context = QMenu()

        #initialization
        self.assign_style_sheet(self.settings.style_sheet)
        self.setup_elements() #Create runtime elements
        self.SetupConnections() #Assign the slots and signal conntections

    def assign_style_sheet(self, path):
        with open(path, 'r') as file:
            self.setStyleSheet(file.read());


    def setup_elements(self):
        #Dock tab widgets
        self.tabifyDockWidget(self.ScriptsWidget, self.GlobalsWidget)
        self.tabifyDockWidget(self.ScriptsWidget, self.TagsWidget)
        self.ScriptsWidget.raise_()
        #Tab Canvas
        self.TabCanvas.tabCloseRequested.connect(self.tab_close)

        #Project dock widget
        #Let the project browser rename files and directories
        self.project_file_browser.setReadOnly(False)
        #Assign the file model to the tree view
        self.ProjectContents.setModel(self.project_file_browser)
        self.ProjectContents.hideColumn(1)
        self.ProjectContents.hideColumn(2)
        self.ProjectContents.hideColumn(3)

        #Context menu creation
        self.ProjectContents.customContextMenuRequested.connect(lambda: ProjectContext.context(self))
        self.project_context_rename = QAction("Rename")
        self.project_context_rename.triggered.connect(lambda: ProjectContext.rename(self))
        self.project_context_delete = QAction("Delete")
        self.project_context_delete.triggered.connect(lambda: ProjectContext.delete(self))
        self.project_context_new = QAction("New File")
        self.project_context_new.triggered.connect(lambda: ProjectContext.new(self))
        self.project_context_collapse_children = QAction("Collapse Child Directories")
        self.project_context_collapse_children.triggered.connect(lambda: ProjectContext.collapse(self))
        self.project_context_expand_children = QAction("Expand Child Directories")
        self.project_context_expand_children.triggered.connect(lambda: ProjectContext.expand(self))
        self.project_context_new_folder = QAction("New Folder")
        self.project_context_new_folder.triggered.connect(lambda: ProjectContext.new_folder(self))
        self.project_context_import = QAction("Import")
        self.project_context_import.triggered.connect(lambda: ProjectContext.Import(self))
        #clear
        return

    #Assign the functions to the slots
    def SetupConnections(self):
        self.file_new.setShortcut("Ctrl+N")                              #File>New
        self.file_new.triggered.connect(lambda: Menu.new(self, self.project, self.settings))
        self.file_open.setShortcut("Ctrl+O")                             #File>Open
        self.file_open.triggered.connect(lambda: Menu.Open(self))
        self.file_open_project.setShortcut("Ctrl+Shift+O")                #File>Open Project
        self.file_open_project.triggered.connect(lambda: Menu.OpenProject(self))
        self.file_save.setShortcut("Ctrl+S")                             #File>Save
        self.file_save.triggered.connect(lambda: Menu.Save(self))
        self.file_save_all.triggered.connect(lambda: self.SaveAll(self))
        self.file_save_all.setShortcut("Ctrl+Shift+S")                     #File>Save As..
        self.file_save_as.triggered.connect(lambda: Menu.SaveAs(self))
        self.file_update.setShortcut("Ctrl+U")                           #File>Update
        self.file_update.triggered.connect(lambda: Menu.Update(self))
        self.file_quit.setShortcut("Alt+F4")                             #File>Quit
        self.file_quit.triggered.connect(lambda: Menu.Quit(self))

        self.edit_undo.setShortcut("Crtl+Z")                             #Edit>Undo
        self.edit_undo.triggered.connect(Menu.Undo)
        self.edit_redo.setShortcut("Crtl+Y")                             #Edit>Redo
        self.edit_redo.triggered.connect(Menu.Redo)
        self.edit_cut.setShortcut("Crtl+X")                              #Edit>Cut
        self.edit_cut.triggered.connect(Menu.Cut)
        self.edit_copy.setShortcut("Crtl+C")                             #Edit>Copy
        self.edit_copy.triggered.connect(Menu.Copy)
        self.edit_paste.setShortcut("Crtl+V")                            #Edit>Paste
        self.edit_paste.triggered.connect(Menu.Paste)

        self.project_new_script.triggered.connect(lambda: Menu.NewScript(self))
        self.project_new_recorded_animation.triggered.connect(Menu.NewRecordedAnimation)
        self.project_build_scripts.setShortcut("F2")                          #Project>Build>Scripts
        self.project_build_scripts.triggered.connect(Menu.BuildScripts)
        self.project_build_map.setShortcut("F3")                              #Project>Build>Build Cache File
        self.project_build_map.triggered.connect(Menu.BuildHaloCache)
        self.project_compile_build.setShortcut("F4")                          #Project>Build>Compile and Build
        self.project_compile_build.triggered.connect(Menu.ScriptCompileAndBuild)
        self.project_import_recorded_animation.setShortcut("Ctrl+Shift+I")     #Project>Import>RecordedAnimation
        self.project_import_recorded_animation.triggered.connect(Menu.ImportRecordedAnimation)
        self.project_import_script.setShortcut("Ctrl+Alt+I")                  #Project>Import>Script
        self.project_import_script.triggered.connect(Menu.ImportScript)
        self.project_bind_scenario.setShortcut("Ctrl+B")                      #Project>Bind Scenario
        self.project_bind_scenario.triggered.connect(Menu.BindScenario)
        self.project_remove_scenario.setShortcut("Ctrl+Shift+B")              #Project>Remove Scenario
        self.project_remove_scenario.triggered.connect(Menu.RemoveBoundScenario)
        self.project_settings.setShortcut("Ctrl+P")                          #Project>Project Settings
        self.project_settings.triggered.connect(Menu.ShowProjectSettings)
        self.help.triggered.connect(Menu.ShowHelp)                          #Help>Help
        self.help_about.triggered.connect(Menu.ShowAbout)                    #Help>About
        self.help_submit_bug.triggered.connect(Menu.SubmitABug)

        self.ScriptView.itemDoubleClicked.connect(self.LoadScriptDbl)
        self.ScriptScope.currentTextChanged.connect(self.ScopeChanged)
        return

    def LoadScriptDbl(self, item, integer):
        tab = TextTab(item.text(integer), "", self.project.scenario_data[0].scripts[item.text(integer)], "hsc")
        tab.isDirty = False
        tab.AddTab(self.TabCanvas)

    def ParseScenarioData(self):
        self.project.load_scenario_data()
        return

    def UpdateUI(self):
        self.scope={}
        for scenario in self.project.scenario_data:
            items = []
            for script in scenario.scripts:
                item = QTreeWidgetItem()
                scriptmeta = scenario.scripts[script][1:scenario.scripts[script].find("\n")].split(" ")
                item.setText(0, scriptmeta[2] if scriptmeta[1] == "static" else scriptmeta[1])
                item.setText(1, scriptmeta[len(scriptmeta) - 1])
                items.append(item)

            for Global in scenario.globals:
                item = QTreeWidgetItem()
                globalmeta = Global.split(" ")
                item.setText(0, globalmeta[1])
                item.setText(1, globalmeta[2])
                if "(" in globalmeta[3]:
                    globalmeta[3] = Global[Global.find("(", 1):Global.find(")", Global.find(")") + 1)]
                else:
                    globalmeta[3] = globalmeta[3].rstrip(")")
                item.setText(2, globalmeta[3])
                self.Globals.addTopLevelItem(item)

            self.scope.update({scenario.scenario_name : items})

        self.ScriptScope.addItems(self.scope.keys())

    def ScopeChanged(self, index):
        for item in self.scope[self.ScriptScope.currentText()]:
            self.ScriptView.addTopLevelItem(item)


    def tab_close(self, i):
        if type(self.TabCanvas.widget(i)) != QWidget:
            if self.TabCanvas.widget(i).isDirty:
                msg = QMessageBox()
                msg.setIcon(QMessageBox.Warning)
                msg.setText("Save changes to " + self.TabCanvas.widget(i).Title + "?")
                msg.setWindowTitle("Save Changes?")
                msg.setStandardButtons(QMessageBox.Save | QMessageBox.No | QMessageBox.Cancel)
                result = msg.exec_()

                if result == QMessageBox.No:
                    self.TabCanvas.removeTab(i)
                    return
                if result == QMessageBox.Save:
                    self.TabCanvas.widget(i).save()
                    self.TabCanvas.removeTab(i)
                if result == QMessageBox.Cancel:
                    return

        self.TabCanvas.removeTab(i)
        return

