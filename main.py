import sys
from PyQt5.QtWidgets import QApplication
from UI.logic.main_window.main_window import MainForm
import os


if __name__ == "__main__":
    app = QApplication(sys.argv)

    #Gather prereqs
    if not os.path.exists("Radium.cfg"):
        os.system("pip install requests python-git PyQt5 PySide")

    #Window definition, and setup
    Window = MainForm()
    Window.showMaximized()

    sys.exit(app.exec_())
