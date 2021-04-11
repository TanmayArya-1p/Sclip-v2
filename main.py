from ui import Ui_MainWindow
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMessageBox
import webbrowser
import sys
import os
import time
from utilities import HotkeyParser,HotkeyChecker
import multiprocessing

url = "https://github.com/TanmayArya-1p/SClip"


class SclipWindow(QtWidgets.QMainWindow):
    
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.transfer_binds = ["Ctrl+T"]
        self.paste_binds = ["Ctrl+B"]
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.Github.clicked.connect(self.OpenGithub)
        self.ui.FileLocation.clicked.connect(self.OpenFileLocation)
        self.ui.SetTransferBind.clicked.connect(self.ToggleTransferEditing)
        self.ui.SetPasteBind.clicked.connect(self.TogglePasteEditing)
        self.ui.Exit.clicked.connect(self.Exit)
        self.ui.exit_option.triggered.connect(self.Exit)
        self.ui.bind_option.triggered.connect(lambda : self.show())

        self.win = self

        with open("binds.env" , "rb") as g:
            handler = str(g.read())[2:-1]
            self.transfer_binds = handler.split(" | ")[1].split(", ")
            self.paste_binds = handler.split(" | ")[0].split(", ")
            print(self.transfer_binds)
            print(self.paste_binds)
            
            self.ui.Transfer_Bind.setEnabled(True)
            self.ui.Paste_Bind.setEnabled(True)
            self.ui.Paste_Bind.setKeySequence(handler.split(" | ")[0])
            self.ui.Transfer_Bind.setKeySequence(handler.split(" | ")[1])
            self.ui.Transfer_Bind.setEnabled(False)
            self.ui.Paste_Bind.setEnabled(False)
            g.close()

        self.__hotkey_thread = multiprocessing.Process(target=HotkeyChecker , args=(self.transfer_binds , self.paste_binds,)  , daemon=True) 
        self.__hotkey_thread.start()
    

        
    def OpenGithub(self):
        webbrowser.open(url)


    def OpenFileLocation(self):
        os.system(f"explorer {os.getcwd()}")


    def ToggleTransferEditing(self):

        if(self.ui.Transfer_Bind.isEnabled()):
            self.ui.Transfer_Bind.setEnabled(False)
            self.ui.SetTransferBind.setText("Set Bind")
            print(self.ui.Transfer_Bind.keySequence().toString())
            self.UpdateBinds()
        else:
            self.ui.Transfer_Bind.clear()
            self.ui.Transfer_Bind.setEnabled(True)
            self.ui.SetTransferBind.setText("Stop Recording")
            
    def TogglePasteEditing(self):
        if(self.ui.Paste_Bind.isEnabled()):
            self.ui.Paste_Bind.setEnabled(False)
            self.ui.SetPasteBind.setText("Set Bind")       
            self.UpdateBinds()
        else:
            self.ui.Paste_Bind.clear()
            self.ui.Paste_Bind.setEnabled(True)
            self.ui.SetPasteBind.setText("Stop Recording")
    
    
    def UpdateBinds(self):
        with open("binds.env" , "w") as j:
            j.write(f"{self.ui.Paste_Bind.keySequence().toString()} | {self.ui.Transfer_Bind.keySequence().toString()}")
            j.close()
        
        self.transfer_binds = list(str(self.ui.Transfer_Bind.keySequence().toString()).split(", "))
        self.paste_binds = list(str(self.ui.Paste_Bind.keySequence().toString()).split(", "))
        print(self.paste_binds)
        print(self.transfer_binds)

        self.__hotkey_thread.terminate()
        self.__hotkey_thread = multiprocessing.Process(target=HotkeyChecker , args=(self.transfer_binds , self.paste_binds, ) , daemon=True) 
        self.__hotkey_thread.start()
    
    def closeEvent(self,event):
        self.hide()
        event.ignore()
    

    def keyPressEvent(self, e):
        print(e.key())
    

    def Exit(self):

        def ex(i):
            if(i.text() == "Cancel"):
                pass
            else:
                sys.exit()

        msg = QMessageBox()
        msg.setWindowTitle("Sclip Exit Confirmation")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("Resources/sclip-logo.ico"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        msg.setWindowIcon(icon)
        msg.setText("Are You Sure You Want To Exit SClip?")
        msg.setIcon(QMessageBox.Warning)
        msg.setStandardButtons(QMessageBox.Yes|QMessageBox.Cancel)
        msg.setDefaultButton(QMessageBox.Cancel)
        msg.buttonClicked.connect(ex)
        msg.exec_()
    
    
    

    
if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = SclipWindow()
    ui.show()
    sys.exit(app.exec_())

    