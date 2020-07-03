from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import os, json, string
from generic.extended_generics import BoolToggle
from IDE.syntax.syntax_highlighting import SyntaxHighlighing

"""                                                                                         "'"
     _______________________________________________________________________________
    |                                                                               |
    |  Last edit: Zatarita(06/23/2020)      ****INCOMPLETE****                      |
    |       CTextEdit(self, text, structure)                                        |
    |       Class handles text editor and autocomplete cooperation                  |
    |           -text is the the text that will be populated into the editor        |
    |           -structure is the definition type that will be used with the file   |
    |                                                                               |
     -------------------------------------------------------------------------------
"""                                                                                         "'"

class CTextEdit(QTextEdit):
    def __init__(self, text="", structure="hsc"):
        QTextEdit.__init__(self)
        self.append(text)
        self.SelectedCompletion = ""
        self.SetupCompleter()

        self.Highlighter = SyntaxHighlighing(self.document(), structure)

        self.CurrentWordPosition = self.textCursor()
        self.cursorPositionChanged.connect(self.CursorMoved)

    def KEY_Tab(self):
        self.ApplyCompletion(self.SelectedCompletion)
        self.Completer.popup().hide()
        return

    def KEY_Space(self):
        if self.Completer.popup().isVisible():
            self.Completer.popup().hide()

    def KEY_Backspace(self):
        self.CurrentWordPosition.movePosition(QTextCursor.PreviousCharacter, QTextCursor.KeepAnchor)
        if self.CurrentWordPosition.selectedText() == ")":
            self.open_lists += 1
        if self.CurrentWordPosition.selectedText() == "(":
            self.open_lists -= 1

    def KEY_Enter(self):
        if self.open_lists > 0:
            self.insertPlainText("    ")
        if self.Completer.popup().isVisible():
            self.Completer.popup().hide()
        #self.CheckLastLine()

    def KEY_OpenQuote(self):
        self.open_quote = BoolToggle(self.open_quote)

    def KEY_OpenBracket(self):
        self.open_lists += 1

    def KEY_CloseBracket(self):
        self.open_lists -= 1
        if self.open_lists == 0:
            self.CurrentWordPosition.movePosition(QTextCursor.StartOfLine, QTextCursor.MoveAnchor)
            self.CurrentWordPosition.movePosition(QTextCursor.NextWord, QTextCursor.KeepAnchor)
            self.CurrentWordPosition.deleteChar()
        return



    def SetupCompleter(self):
        self.Completer = CompleterDictionary()
        self.Completer.setWidget(self)
        self.Completer.setCaseSensitivity(Qt.CaseSensitive)
        self.Completer.setCompletionMode(QCompleter.PopupCompletion)

        self.open_quote = False
        self.open_lists = 0

        self.KeyHandler = { Qt.Key_ParenLeft  : self.KEY_OpenBracket,
        Qt.Key_ParenRight : self.KEY_CloseBracket,
        Qt.Key_QuoteDbl   : self.KEY_OpenQuote,
        Qt.Key_Space      : self.KEY_Space,
        Qt.Key_Backspace  : self.KEY_Backspace,
        Qt.Key_Return     : self.KEY_Enter,
        Qt.Key_Enter      : self.KEY_Enter,
        Qt.Key_Tab        : self.KEY_Tab
        }

        self.Completer.insertText.connect(self.ApplyCompletion)
        self.Completer.highlighted.connect(self.CompleterSelectionChanged)

    def CursorMoved(self):
        pass

    def mousePressEvent(self, event):
        self.CheckLastLine()
        super(CTextEdit, self).mousePressEvent(event)


    def keyPressEvent(self, event):
        super(CTextEdit, self).keyPressEvent(event)

        KeyHandle = self.KeyHandler.get(event.key(), None)
        if KeyHandle != None:
            if KeyHandle():
                return

        self.CurrentWordPosition.select(QTextCursor.WordUnderCursor)
        self.Completer.setCompletionPrefix(self.CurrentWordPosition.selectedText())

        if self.Completer.completionCount() == 0:
            self.Completer.popup().hide()
        else:
            self.Completer.popup().selectionModel().select(self.Completer.completionModel().index(0,0), QItemSelectionModel.Select)

        for letter in list(string.ascii_lowercase) + list(string.ascii_uppercase):
            if event.text() == letter and not self.Completer.popup().isVisible() and self.Completer.completionCount() != 0 and not self.open_quote:
                self.Completer.popup()
                rect = self.cursorRect()
                rect.setWidth(200)
                self.Completer.complete(rect)


    def CompleterSelectionChanged(self, text):
        self.SelectedCompletion = text

    def ApplyCompletion(self, text):
        self.CurrentWordPosition.insertText(text)
        self.setTextCursor(self.CurrentWordPosition)

    def CheckLastLine(self):
        self.CurrentWordPosition.movePosition(QTextCursor.StartOfLine, QTextCursor.MoveAnchor)
        self.CurrentWordPosition.movePosition(QTextCursor.EndOfLine, QTextCursor.KeepAnchor)
        quotecount = 0
        openbracket = 0
        closebracket = 0

        for character in self.CurrentWordPosition.selectedText():
            if character == '"':
                quotecount += 1

            if character == '(':
                openbracket += 1
            if character == ')':
                closebracket += 1

        self.CurrentWordPosition.clearSelection()



class CompleterDictionary(QCompleter):
    """                                                                                         "'"
         _______________________________________________________________________________
        |                                                                               |
        |  Last edit: Zatarita(06/11/2020)                                              |
        |       CompleterDictionary.AutoCompleteBlock(self, block)                      |
        |       Class holds autocomplete definitions.                                   |
        |           -block is the the definition chunk loaded for .acd file             |
        |                                                                               |
        |   "See IDE/AutoComplete/Definitions/block documentation.txt" for more info    |
        |                                                                               |
         -------------------------------------------------------------------------------
    """                                                                                         "'"
    class AutoCompleteBlock():
        Identifier = ""
        Return = {}
        Arguments = {}
        Description = ""

        def __init__(self, block=None):
            if not block == None:
                self.ParseBlock(block)

        def ParseBlock(self, block):
            if len(block.split(" : ")) == 2:
                self.Return, self.Identifier = block.split(" : ")
                if self.Return == "KEYWRD" or self.Return == "DTATYP":
                    return True

            if not len(block.split(" : ")) == 4:
                print("Invalid block syntax: ("+block+")")
                return False


            returns, self.Identifier, arguments, self.Description = block.split(" : ")
            for ret in returns.split(", "):
                self.Return.update(self.ExtractSubBlockNames(ret, self))
            for arg in arguments.split(", "):
                self.Arguments.update(self.ExtractSubBlockNames(arg, self))
            return True

        def ExtractSubBlockNames(self, SubBlock, parent):
            if SubBlock.find("=") == -1:            #If the Sub Block doesnt have a name
                if SubBlock == "void" or SubBlock == "none":
                    return {SubBlock : "NULL"}          #Return the subblock with a null name if none or void
                print("Unable to load subBlock: ("+parent.Identifier+") - Non-void block ("+SubBlock+") not given a name")
                return {"" : ""}                    #Throw an error, and return an empty block.
            ret, name = SubBlock.split("=")         #If everything is ok, Strip out the names
            return {ret : name}                     #And return the identifier : name dictionary entry

    """                                                                                         "'"
         _______________________________________________________________________________
        |                                                                               |
        |  Last edit: Zatarita(06/11/2020)                                              |
        |       CompleterDictionary(self, path)                                         |
        |       Class handles the QCompleter and loads in the definitions               |
        |           -Path is path to the .acd file that holds the autocomplete data     |
        |                                                                               |
        |   "See IDE/AutoComplete/Definitions/block documentation.txt" for more info    |
        |                                                                               |
         -------------------------------------------------------------------------------
    """                                                                                         "'"
    insertText = pyqtSignal(str)
    Dictionary = []

    def __init__(self, path = os.getcwd() + "/IDE/auto_complete/definitions/hsc/hsc.acd"):
        self.LoadDictionary(path)
        QCompleter.__init__(self, [self.Dictionary[x].Identifier for x in range(len(self.Dictionary))], None)
        self.activated.connect(self.CompleterActivated)

    def LoadDictionary(self, path):
        if not os.path.exists(path):
            print("Unable to locate file: " + path)
            return
        with open(path, "r") as File:
            for line in File:
                if "`" in line:
                    type, variables = line.split(" : ")
                    variables = variables.split(" ` ")
                    for var in variables:
                        var = var.rstrip("\n")
                        self.Dictionary.append(self.AutoCompleteBlock(type + " : " + var))
                    continue
                self.Dictionary.append(self.AutoCompleteBlock(line))

    def CompleterActivated(self, text):
        print(text)
        self.insertText.emit(text)
