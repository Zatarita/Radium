from PyQt5.QtGui import QCursor
from PyQt5.QtWidgets import QFileDialog
from PyQt5.QtCore import QFileInfo
import shutil

class ProjectContext():
    #Context Definition
    def context(self):
        if "Folder" in self.ProjectContents.selectedIndexes()[0].siblingAtColumn(2).data():
            self.project_browser_context.addAction(self.project_context_expand_children)
            self.project_browser_context.addAction(self.project_context_collapse_children)
            self.project_browser_context.addSeparator()
            self.project_browser_context.addAction(self.project_context_import)
            self.project_browser_context.addAction(self.project_context_new)
            self.project_browser_context.addAction(self.project_context_new_folder)
            self.project_browser_context.addSeparator()
            self.project_browser_context.addAction(self.project_context_rename)
            self.project_browser_context.addAction(self.project_context_delete)
            if self.ProjectContents.selectedIndexes()[0].siblingAtColumn(0).data() == "Scripts":
                self.ProjectContents_ContextDeleteDirectory.setEnabled(False)

        self.project_browser_context.exec_(QCursor().pos());
        return

    #Context rename function
    def rename(self):
        self.ProjectContents.edit(self.ProjectContents.selectedIndexes()[0])
        return

    #Context delete function
    def delete(self):
        confirmation = QMessageBox.question(self,'', "Are you sure you want to delete this directory?", QMessageBox.Yes | QMessageBox.No)
        if confirmation == QMessageBox.Yes:
            shutil.rmtree(self.project_browser_context.filePath(self.ProjectContents.selectedIndexes()[0]))
        return

    #Context New Function
    def new(self):
        open(self.project_browser_context.filePath(self.ProjectContents.selectedIndexes()[0]) + "/", "w")
        index = self.project_browser_context.index(self.project_browser_context.filePath(self.ProjectContents.selectedIndexes()[0]) + "/ ")
        self.ProjectContents.setCurrentIndex(index)
        self.ProjectContents.edit(self.ProjectContents.selectedIndexes()[0])
        return

    #Context Collapse Function
    def collapse(self):
        self.ProjectContents.collapseAll()
        return

    #Context Expand Function
    def expand(self):
        self.ProjectContents.expandAll()
        return

    #Context Import Function
    def import_item(self):
        file, _ = QFileDialog.getOpenFileName(self,"Import File", "", "All Files (*.*)")
        file_info = QFileInfo(file)
        shutil.copyfile(file, self.project_browser_context.filePath(self.ProjectContents.selectedIndexes()[0]) + "/" + file_info.fileName())
        return

    #New Folder
    def new_folder(self):
        os.mkdir(self.project_browser_context.filePath(self.ProjectContents.selectedIndexes()[0]) + "/ ")
        index = self.project_browser_context.index(self.project_browser_context.filePath(self.ProjectContents.selectedIndexes()[0]) + "/ ")
        self.ProjectContents.setCurrentIndex(index)
        self.ProjectContents.edit(self.ProjectContents.selectedIndexes()[0])
        return
