from PyQt5.QtWidgets import QGridLayout

from UI.logic.widgets.tabs.tab_generic import TabGeneric
from IDE.auto_complete.auto_complete import CTextEdit

class TextTab(TabGeneric):
    def __init__(self, title, path, data = "", structure = ""):
        TabGeneric.__init__(self, title, path, data)
        self.dirty = False

        self.text_box = CTextEdit(self.data, structure)
        self.layout = QGridLayout()
        self.layout.addWidget(self.text_box)
        self.setLayout(self.layout)

        self.text_box.textChanged.connect(self.text_changed)

    def text_changed(self):
        self.dirty = True

    def save(self):
        if self.path == "":
            self.path, _ = QFileDialog.getSaveFileName(self, "Save File", "", "Halo Script (*.hsc);;Syntax Definiton (*.def);;Lua Script (*.lua);;Text Document (*.txt)")
        with open(self.Path, 'w') as file_out:
            file_out.write(self.text_box.toPlainText())
