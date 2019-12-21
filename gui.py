from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtMultimedia import *
from PyQt5.QtMultimediaWidgets import *
from mainWindow import Ui_MainWindow
import sys,os,logging
from pathlib import Path

MANIM_DIRECTORY = Path("c://Users/jaybo/OneDrive/Documents/Manim")

class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        self.setupUi(self)

        # Show stacked widget for each preset animation
        self.presetCombo.currentIndexChanged.connect(self.display)
        
        # Compile preset animation
        self.compilePresetButton.clicked.connect(self.compilePreset)

        self.show()  
    
    # Procedure to show stacked widget
    def display(self,i):
        self.presetStack.setCurrentIndex(i)
    
    # Procedure to compile
    @pyqtSlot()
    def compilePreset(self):
        path1 = MANIM_DIRECTORY / "manim.py"
        path2 = MANIM_DIRECTORY / "manimgui" / "presets.py"
        command_string = "python " + path1.absolute().as_posix() + " " + path2.absolute().as_posix()
        print(command_string)
        fname = MANIM_DIRECTORY / "manimgui" / "temp.py"
        # Complex function
        if self.presetCombo.currentIndex() == 1:
            command_string += " ComplexFunction"
            with open(fname, 'w') as f:
                f.writelines([
                    "import numpy as np\n",
                    "complex_func = lambda z : ",
                    self.le_complex_func.text()
                ])
        # Slope and Derivative
        elif self.presetCombo.currentIndex() == 2:
            command_string += " SlopeAndDerivative"
            with open(fname, 'w') as f:
                f.writelines([
                    "import numpy as np\n",
                    "real_func = lambda x : ",
                    self.le_real_func.text()
                ])
        # Linear Transformation
        elif self.presetCombo.currentIndex() == 3:
            command_string += " LinearTransformation"
            temp = ""
            if self.showBasisCheck.isChecked()==True:
                temp += "show_basis_vectors = True\n"
            with open(fname, 'w') as f:
                f.writelines([
                    temp,
                    "linear_transf = [[",
                    self.table_linear_transf.item(0,0).text(), ",", self.table_linear_transf.item(0,1).text(), "],[",
                    self.table_linear_transf.item(1,0).text(), ",", self.table_linear_transf.item(1,1).text(), "]]"
                ])
        else:
            print("Please select an animation to continue.")
            return
        if self.checkBox_2.isChecked()==True:
            command_string += " -p"
            if self.checkBox.isChecked()==False:
                command_string += "l"
        elif self.checkBox.isChecked()==False:
            command_string += " -l"
        os.system(command_string)
    
if __name__ == '__main__':
    app = QApplication([])

    window = MainWindow()
    app.exec_()