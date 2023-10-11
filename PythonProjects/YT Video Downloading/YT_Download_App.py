#The purpose of this file will be to download youtube videos, when giving a video URL.

#Import Modules
from pytube import YouTube

#GUI Modules
from PyQt6.QtWidgets import (
    QMainWindow, QApplication, QPushButton,
    QAbstractButton, QLineEdit, QLabel,
    QHBoxLayout, QVBoxLayout, QGridLayout,
    QWidget
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QGuiApplication, QFont

class MainWindow(QMainWindow):

    #------------------------
    # GUI Creation Functions
    #------------------------

    #Create left hand section for the video file name display.
    def createLeftSection(self):
        #TODO: Create the widgets and layouts for this section. 
        self.leftSection = QVBoxLayout()
        self.videoNameContainer = QVBoxLayout()

        allVideosLabel = QLabel("Current Videos")
        
        videoLabelFont = QFont()
        videoLabelFont.setPointSize(24)

        allVideosLabel.setFont(videoLabelFont)

        self.leftSection.addWidget(allVideosLabel)
        
        self.leftSection.setAlignment(Qt.AlignmentFlag.AlignHCenter)

    #Create the main display for the downloading of the youtube video. This should include the progress bar, and the input field for the youtube link. May add more later
    def createMainSection(self):
        #TODO: Create the widgets and layouts for this section. 
        pass

    #Create the area to host the thumbnail image of the video. This section is the most open and will probably end up hosting more later
    def createRightSection(self):
        #TODO: Create the widgets and layouts for this section. 
        pass

    #Combine all previous layouts and set the main window's central widget to be a QWidget object with it's layout set to the combined layout.
    def __init__(self):
        #TODO: Combine all layouts here and set the main windows central widget to a QWidget with the combined layout.
        #Calls parent constructor to create the window
        super(MainWindow, self).__init__()
        self.setWindowTitle("YT Video Download Application")

        #Forces the window to the full screen size.
        screen_resolution = QGuiApplication.primaryScreen().availableGeometry()
        width, height = screen_resolution.width(), screen_resolution.height()
        self.widthScale = width / 1920
        self.heightScale = height / 1032
        self.setFixedSize(int(self.widthScale * 1920), int(self.heightScale * 1032))
        
        #Forces the window to be centered on the screen
        screen_rect = QGuiApplication.primaryScreen().geometry()
        window_rect = self.frameGeometry()
        window_rect.moveCenter(screen_rect.center())
        window_rect.moveTop(0)
        self.move(window_rect.topLeft())

        #Create Each Section of the Application
        self.createLeftSection()
        self.createMainSection()
        self.createRightSection()

        self.mainLayout = QHBoxLayout()

        self.mainLayout.addLayout(self.leftSection)

        centralWidget = QWidget()
        centralWidget.setLayout(self.mainLayout)

        self.setCentralWidget(centralWidget)

    #------------------------
    #Start-up Functions
    #------------------------

    #------------------------
    #Slot Functions
    #------------------------



#Main Function. Creates the Application
if __name__ == "__main__":
    app = QApplication([])

    window = MainWindow()
    window.show()
    
    app.exec()