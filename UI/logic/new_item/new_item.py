# This Python file uses the following encoding: utf-8
from PyQt5.QtWidgets import QWidget, QDialog, QFileDialog
from PyQt5 import QtGui, uic
import os
from UI.logic.new_item.sub.advanced import NewProjectAdvancedDialog
from UI.logic.new_item.sub.bind import NewProjectBind

class NewItemDialog(QDialog):
    def __init__(self, parent = None):
        QWidget.__init__(self, parent)

        self.new_project_advanced = NewProjectAdvancedDialog()
        self.bind_scenarios = NewProjectBind()

        uic.loadUi('UI/design/new_item/new_item.ui', self)
        self.setup_connections()
        self.setup_elements()
        return

    def setup_connections(self):
        self.AdvancedProjectSettings.clicked.connect(self.ShowAdvancedSettings)
        self.BindScenarios.clicked.connect(self.show_bind_scenarios)
        self.DialogOkCancel.accepted.connect(self.accept_clicked)
        self.BrowseProjectDirectory.clicked.connect(self.project_browse)
        self.BrowseLocalScriptDirectory.clicked.connect(self.script_browse)
        self.BrowseLocalRecordedAnimationDirectory.clicked.connect(self.recorded_animation_browse)
        self.BrowseBackupDirectory.clicked.connect(self.backup_browse)
        return

    def setup_elements(self):
        return

    def ShowAdvancedSettings(self):
        self.new_project_advanced.exec_()
        return

    def accept_clicked(self):
        if not self.ProjectName.text() == "":
            self.accept()
        return

    def show_bind_scenarios(self):
        self.bind_scenarios.exec_()
        return

    def project_browse(self):
        self.ProjectDirectory.setText(QFileDialog.getExistingDirectory(self, "Open Directory"))
        return


    def script_browse(self):
        self.ScriptsDirectory.setText(QFileDialog.getExistingDirectory(self, "Open Directory"))
        return


    def recorded_animation_browse(self):
        self.RecordedAnimationsDirectory.setText(QFileDialog.getExistingDirectory(self, "Open Directory"))
        return


    def backup_browse(self, project = None):
        self.BackupDirectory.setText(QFileDialog.getExistingDirectory(self, "Open Directory"))
        return
