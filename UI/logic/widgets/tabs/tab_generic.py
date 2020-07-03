from PyQt5.QtWidgets import QWidget

class TabGeneric(QWidget):
    def __init__(self, title, path, data):
        QWidget.__init__(self)
        self.title = title
        self.data = data
        self.path = path

    def AddTab(self, canvas):
        canvas.setCurrentIndex(canvas.addTab(self, self.title))

    def Save(self):
        return
