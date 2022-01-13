import PyQt5.QtWidgets as qtw
# from PyQt5.QtCore import QObject, QThread, pyqtSignal
import tools as tl
import sys

class MainWindow(qtw.QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('ToolBox')
        self.setWindowOpacity(0.99)
        self.setStyleSheet("background-color: #1f1f1f;")
        self.setLayout(qtw.QVBoxLayout())
        self.maingrid()
        self.show()

    def maingrid(self):
        container = qtw.QWidget()
        container.setLayout(qtw.QGridLayout())
        container.setStyleSheet("padding: 8px; QInputDialog {background-color: #bababa;}")
        container.setSizePolicy(qtw.QSizePolicy.Expanding, qtw.QSizePolicy.Expanding)

        self.urlbox = qtw.QLineEdit()
        self.urlbox.setPlaceholderText("Enter YouTube URL")
        container.layout().addWidget(self.urlbox, 0, 0, 0, 6)

        getdir = qtw.QPushButton("File Destination", clicked = lambda: self.getdir())
        # getdir.setSizePolicy(qtw.QSizePolicy.Expanding, qtw.QSizePolicy.Expanding)
        container.layout().addWidget(getdir, 0, 9)

        download = qtw.QPushButton("Download", self)
        download.clicked.connect(self.dl_execute)
        # download.setSizePolicy(qtw.QSizePolicy.Expanding, qtw.QSizePolicy.Expanding)
        container.layout().addWidget(download, 0, 10)

        self.layout().addWidget(container, stretch = 1)

    def getdir(self):
        self.fileloc = str(qtw.QFileDialog.getExistingDirectory(self, "Select Directory"))
        
    def dl_execute(self):
        try:
            self.urlboxval = self.urlbox.text()
            tl.dl_execute(self.urlboxval, self.fileloc)
        except:
            print("No URL or no destination")

if __name__ == '__main__':
    app = qtw.QApplication(sys.argv)
    mw = MainWindow()
    mw.setMinimumSize(600, 100)
    mw.setMaximumSize(800, 100)
    app.setStyle(qtw.QStyleFactory.create('Fusion'))
    app.setStyleSheet("QPushButton, QLabel, QLineEdit, QComboBox, QAbstractItemView, QMessageBox, QToolTip {color: #c7c7c7;}")
    app.exec_()
    app.quit()