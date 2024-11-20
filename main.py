# 程序入口

import sys
from PyQt5 import QtWidgets
from pythonCode import window
from pythonCode import collect

def main():
    APP = QtWidgets.QApplication([])
    desktopObj = APP.desktop()
    width = int(desktopObj.width()/4)
    height = int(desktopObj.height()/4)
    mainWindow = window.Window(width,height)
    mainWindow.show()
    print(collect.configBase["APP_WELCOME"])
    sys.exit(APP.exec_())

if __name__ == "__main__": main()
