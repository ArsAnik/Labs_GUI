import sys
import os
import PyQt5
from PyQt5.QtWidgets import (QWidget, QPushButton, QLabel, QApplication, QDesktopWidget)
from PyQt5.QtGui import QPixmap
from PyQt5.QtGui import QFont

# Windows fix
pyqt_dir = os.path.dirname(PyQt5.__file__)
os.environ["QT_QPA_PLATFORM_PLUGIN_PATH"] = os.path.join(pyqt_dir, "Qt5", "plugins")

class ShowImageWindow(QWidget):

    def __init__(self):
        super().__init__()
        self.isImageShown = False
        self.initUI()


    def initUI(self):
        
        self.center()
        self.resize(400, 560)

        self.label = QLabel(self)
        self.setStyleSheet("background-color: #fff;")
        font = QFont("Calibri", 16)
        self.label.setFont(font)
        self.showText()

        self.button = QPushButton("Показать кота!", self)
        self.button.clicked.connect(self.ButtonHandler)
        self.button.resize(400, 50)
        self.button.setFont(font)
        self.button.move(0, 505)


    def center(self):

        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())


    def showText(self):

        self.label.clear()
        self.label.setText("Показать кота!")
        self.label.move(150, 0)
        self.label.adjustSize()


    def showImage(self):

        self.label.clear()
        iamge = QPixmap("img.jpg")
        self.label.setPixmap(iamge)
        self.label.move(0, 0) 
        self.label.adjustSize()


    def ButtonHandler(self):

        if self.isImageShown:
            self.showText()
        else:
            self.showImage()

        self.isImageShown = not self.isImageShown


if __name__ == '__main__':

    app = QApplication(sys.argv)
    window = ShowImageWindow()
    window.show()
    sys.exit(app.exec_())