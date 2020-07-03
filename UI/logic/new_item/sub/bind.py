from PyQt5.QtWidgets import QWidget, QDialog, QListWidgetItem, QFileDialog
from PyQt5 import QtGui, uic
from PyQt5.QtCore import QFileInfo
import os

class NewProjectBind(QDialog):
    def __init__(self, parent = None):
        QWidget.__init__(self, parent)

        uic.loadUi('UI/design/new_item/sub/bind.ui', self)
        self.SetupConnections(self)
        return

    def SetupConnections(self, parent = None):
        self.AddItem.clicked.connect(self.AddItemToList)
        self.RemoveItem.clicked.connect(self.RemoveItemFromList)
        self.BatchImport.clicked.connect(self.Batch)
        return

    def AddItemToList(self):
        FileName, _ = QFileDialog.getOpenFileName(self,"Open Scenario", "", "Scenarios (*.scenario)")
        self.ScenarioList.addItem(FileName)
        return

    def RemoveItemFromList(self):
        SelectedItems = self.ScenarioList.selectedItems()
        if not SelectedItems : return
        for Item in SelectedItems:
            self.ScenarioList.takeItem(self.ScenarioList.row(Item))
        return

    def Batch(self, parent = None):
        Scenarios = []
        for dirpath, dirnames, filenames in os.walk(QFileDialog.getExistingDirectory(self, "Open Directory")):
            for filename in [f for f in filenames if f.endswith(".scenario")]:
                self.ScenarioList.addItem(os.path.join(dirpath, filename))
        return
