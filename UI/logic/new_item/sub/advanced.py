from PyQt5.QtWidgets import QWidget, QDialog
from PyQt5 import QtGui, uic

class NewProjectAdvancedDialog(QDialog):
    def __init__(self, parent = None):
        QWidget.__init__(self, parent)

        uic.loadUi('UI/design/new_item/sub/advanced.ui', self)
        self.SetupConnections(self)
        return

    def SetupConnections(self, parent = None):
        return
