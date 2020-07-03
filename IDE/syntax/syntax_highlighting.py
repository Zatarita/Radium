from PyQt5.QtCore import QRegExp
from PyQt5.QtGui import QColor, QTextCharFormat, QFont, QSyntaxHighlighter
import os, json


class SyntaxHighlighing(QSyntaxHighlighter):
    """                                                                                         "'"
             _______________________________________________________________________________
            |                                                                               |
            |  Last edit: Zatarita(07/03/2020)                                              |
            |       SyntaxHighlighing.ColorGroup(self, parent, palette, functions)          |
            |       ColorGroups handle linking keywords to color palettes                   |
            |           -Parent is the SyntaxHighlighting class that holds the ColorGroup   |
            |           -palette is a list hold RGB, and a font modifier (1= bold,2= italic)|
            |           -functions is a list of identifiers the palette is applied to       |
            |                                                                               |
             -------------------------------------------------------------------------------
    """                                                                                         "'"
    #initialize ColorGroup: Create color from RGB, assign color and font style
    class ColorGroup():
        def __init__(self, parent, palette, identifier):
            self.identifier = identifier
            self.format = QTextCharFormat()
            self.expressions = []
            #Verify color data and identifier
            if not parent.verify((palette, identifier)):
                return
            #assign the font color
            self.format.setForeground(QColor(palette[0], palette[1], palette[2]))
            #assign the font styling
            if palette[3] == 1:
                self.format.setFontWeight(QFont.Bold)
            if palette[3] == 2:
                self.format.setFontItalic(True)
            #Create and assign QRegExp. (Please don't try to hard to understand this nightmare)
            for id in self.identifier:
                #Special case STRING
                if id == "STRING":
                    self.expressions.append(QRegExp("\"(\\\\\"|[^\"])+\""))
                #Special case NUMBER
                elif id == "NUMBER":
                    self.expressions.append(QRegExp("\d*\d"))
                    self.expressions.append(QRegExp("\\d*\\.\\d+"))
                #Special case escape character
                elif len(id.split("$")) > 1:
                    _, stripped_name = id.split("$")
                    self.expressions.append(QRegExp("\\" + stripped_name +"*"))
                #Regular case
                else:
                    self.expressions.append(QRegExp("\\b" + str(id) + "\\b"))
            return
    """                                                                                         "'"
             _______________________________________________________________________________
            |                                                                               |
            |  Last edit: Zatarita(06/11/2020)                                              |
            |       SyntaxHighlighing(self, parent, theme)                                  |
            |       Class holds all functions relating to syntax based text highlighting    |
            |           -Parent is the QTextEdit that holds the text data                   |
            |           -Theme is the palette data to be loaded                             |
            |                                                                               |
             -------------------------------------------------------------------------------
    """                                                                                         "'"
    color_groups = []


    #Initialize SyntaxHighlighting: Load the theme, and assign the ColorGroups
    def __init__(self, parent, theme):
        QSyntaxHighlighter.__init__( self, parent )
        #Default definitions directory is /IDE/Syntax/Definitions/
        path = os.getcwd() + "/IDE/syntax/definitions/" + theme + "/" + theme + ".def"
        #Verify if file exists, and if there are an even number of rows
        if not self.verify(path):
            return
        #load each line, and interpret the list to a new ColorGroup
        with open(path, "r") as ReadFile:
            for line in ReadFile:
                self.color_groups.append(self.ColorGroup(self, json.loads(line), json.loads(ReadFile.readline().rstrip("\n"))))

    #Add a new expression with a specific palette to the ColorGroups
    def AddExpressions(self, palette, expression):
        #Verify the palette, and expression
        if not self.verify((palette, expression)):
            return
        #Add the new identifier to the color groups
        self.color_groups.append(self.ColorGroup(color, expression))
        return


    #Handles applying the highlighting
    def highlightBlock(self, text):
        for group in self.color_groups:
            for expression in group.expressions:
                #Search for each instance of an expression, and return the index if found
                index = expression.indexIn(text)
                while index >= 0:
                    #assign the font format for the found instance, and check for more
                    self.setFormat(index, expression.matchedLength(), group.format)
                    index = expression.indexIn(text, index + expression.matchedLength() + 1)
        self.setCurrentBlockState(0)


    #Data integrity
    def verify(self, data):
        #tuple is ColorGroup data (palette, function)
        if type(data) == tuple:
            palette, functions = data
            for func in functions:
                #ERROR: non-string item in the functions list
                if type(func) != str:
                    print("[!] Color Group data is incorrectly formatted: Non-string values found in functions array")
                    return False
            for pal in palette:
                if type(pal) != int:
                    #ERROR: Non-integer item in color pallet
                    print("[!] Color Group data is incorrectly formatted: Non-integer values found in palette array")
                    return False
            if len(palette) != 4:
                #ERROR: palette legnth invalid
                print("[!] Color palette data is incorrectly formatted: Color data size is" + str(len(palette)) + ". Expected size is 4")
                return False
            for i in range(3):
                if palette[i] > 255:
                    #ERROR: RGB values exceed 255
                    print("[!] Color palette data is incorrectly formatted: Element " + str(i) + " is greater than 255")
                    return False
            if palette[3] > 2:
                #WARNING: Font style unrecognized (0, none, 1 bold, 2 italic, 3+ undefined)
                print("[_] Color palette data is incorrectly formatted: Element 4 is greater than 2")
                return True
        if type(data) == str:
            #string is file path
            if not os.path.exists(data):
                #ERROR: File path doesn't exist
                print("[!] File could not be found: " + data)
                return False
            if (len(open(data).readlines()) & 1) == 1:
                #ERROR: File has odd numbers of lines
                print("[!] File could not be loaded: Color group is missing pair.")
                return False

        return True
