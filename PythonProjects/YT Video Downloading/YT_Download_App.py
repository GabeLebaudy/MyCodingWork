#The purpose of this file will be to download youtube videos, when giving a video URL.

#Import Modules
from pytube import YouTube
import guiConstants
import os
import urllib.request

#GUI Modules
from PyQt6.QtWidgets import (
    QMainWindow, QApplication, QPushButton,
    QAbstractButton, QLineEdit, QLabel,
    QHBoxLayout, QVBoxLayout, QGridLayout,
    QWidget, QSpacerItem, QAbstractSpinBox,
    QSizePolicy, QComboBox, QFileDialog,
    QDialog, QDialogButtonBox
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QGuiApplication, QFont, QColor, QPalette, QPixmap

#Create Widget filled with color (Used for progress bar)
class Color(QWidget):
    #Constructor
    def __init__(self, color):
        super(Color, self).__init__()
        
        self.setAutoFillBackground(True) #Fill entire widget with color
        
        palette = self.palette()
        palette.setColor(QPalette.ColorRole.Window, QColor(color))
        self.setPalette(palette)

#Main Window
class MainWindow(QMainWindow):

    #------------------------
    # GUI Creation Functions
    #------------------------

    #Create left hand section for the video file name display.
    def createLeftSection(self): 
        #Main layout for section
        self.leftSection = QVBoxLayout()

        #Will add widgets to the container, this layout will contain video names from the current output folder
        self.videoNameContainer = QVBoxLayout()

        #Create label for section
        allVideosLabel = QLabel("Current Videos")
        videoLabelFont = QFont()
        videoLabelFont.setPointSize(20)
        videoLabelFont.setUnderline(True)
        allVideosLabel.setFont(videoLabelFont)
        
        #Put together layout
        self.leftSection.addSpacerItem(QSpacerItem(0, int(100 * self.heightScale), QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed))
        self.leftSection.addWidget(allVideosLabel)
        self.leftSection.setAlignment(Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignTop)

    #Create the main display for the downloading of the youtube video. This should include the progress bar, and the input field for the youtube link. May add more later
    def createMainSection(self):
        #Define main layout for this section
        self.mainSection = QVBoxLayout()

        #Define sub-layouts for this section
        self.titleContainer = QHBoxLayout()
        self.urlContainer = QHBoxLayout()
        self.downloadBarContainer = QHBoxLayout()
        self.downloadInfoLayout = QHBoxLayout()
        self.chooseFolderContainer = QHBoxLayout()
        self.chooseFormatContainer = QHBoxLayout()
        
        #Title Section: This section will serve as a display and also provide a help button to explain features
        titleLabel = QLabel("Download YT Videos")
        titleFont = QFont()
        titleFont.setPointSize(32)
        titleLabel.setFont(titleFont)

        self.explainationButton = QPushButton("?") #This button will explain the purpose of the application to the user.
        self.explainationButton.setFixedSize(int(40), int(40))
        self.explainationButton.setStyleSheet(guiConstants.HELPBUTTONSTYLE)

        self.titleContainer.addWidget(titleLabel)
        self.titleContainer.addSpacerItem(QSpacerItem(int(15 * self.widthScale), 0, QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Minimum))
        self.titleContainer.addWidget(self.explainationButton)
        self.titleContainer.setAlignment(Qt.AlignmentFlag.AlignHCenter)

        #URL Input Section: This section will provide an input for the URL of a video to download
        urlLabel = QLabel("Video URL:")
        urlFont = QFont()
        urlFont.setPointSize(16)
        urlLabel.setFont(urlFont)

        self.urlInput = QLineEdit()
        self.urlInput.setFixedWidth(int(500 * self.widthScale))
        self.urlInput.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        self.urlInput.returnPressed.connect(self.downloadVideo)

        self.urlButton = QPushButton("Download")
        self.urlButton.setFixedSize(int(75 * self.widthScale), int(25 * self.heightScale))
        self.urlButton.clicked.connect(self.downloadVideo)

        self.urlContainer.addWidget(urlLabel)
        self.urlContainer.addWidget(self.urlInput)
        self.urlContainer.addWidget(self.urlButton)
        self.urlContainer.setAlignment(Qt.AlignmentFlag.AlignHCenter)

        #Download Bar Section: This section will display the current progress of the video download. 

        #TODO: Incorporate section for displaying that the file type is changing if that takes a signifigant portion of time to complete.
        progressBarLabel = QLabel("Progress: (0%)")
        progressBarLabel.setFont(urlFont)

        self.progressBarComplete = Color('#6ef246')
        self.progressBarIncomplete = Color('#4a4f48')

        self.progressBarComplete.setFixedSize(0, int(30 * self.heightScale))    
        self.progressBarIncomplete.setFixedSize(int(553 * self.widthScale), int(30 * self.heightScale))

        self.downloadBarContainer.addWidget(progressBarLabel)
        self.downloadBarContainer.addWidget(self.progressBarComplete)
        self.downloadBarContainer.addWidget(self.progressBarIncomplete)
        self.downloadBarContainer.setAlignment(Qt.AlignmentFlag.AlignHCenter)

        #Download Information Section: This area will display info about the download process to the user
        statusLabel = QLabel("Status:")
        statusFont = QFont()
        statusFont.setPointSize(12)
        statusLabel.setFont(statusFont)

        self.downloadInfoLabel = QLabel()
        self.downloadInfoLabel.setFont(statusFont)

        self.downloadInfoLayout.addWidget(statusLabel)
        self.downloadInfoLayout.addWidget(self.downloadInfoLabel)
        self.downloadInfoLayout.setAlignment(Qt.AlignmentFlag.AlignLeft)

        #Select Output Folder Section: This section allows the user to choose where the downloaded folders are stored
        selectFolderLabel = QLabel("Current Output Folder:")
        selectFolderLabel.setFont(urlFont)

        self.selectFolderInput = QLineEdit()
        self.selectFolderInput.setFixedWidth(int(325 * self.widthScale))
        self.selectFolderInput.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        self.selectFolderInput.setReadOnly(True)
        self.fillOutputFolderDisplay()

        self.changeFolderButton = QPushButton("Change Output Folder")
        self.changeFolderButton.setFixedSize(int(150 * self.widthScale), int(25 * self.heightScale))
        self.changeFolderButton.clicked.connect(self.chooseOutputFolder)

        self.chooseFolderContainer.addWidget(selectFolderLabel)
        self.chooseFolderContainer.addWidget(self.selectFolderInput)
        self.chooseFolderContainer.addWidget(self.changeFolderButton)
        self.chooseFolderContainer.setAlignment(Qt.AlignmentFlag.AlignHCenter)

        #Choose File Type Section: This section will allow the user to choose the file extension if they want to switch from the default
        chooseFileTypeLabel = QLabel("File Type")
        chooseFileTypeLabel.setFont(urlFont)

        #TODO: Make the text align to the right in the combo box
        self.selectFileTypeDD = QComboBox()
        fileTypeOptions = ['.mp4', '.wav']
        self.selectFileTypeDD.addItems(fileTypeOptions)
        self.selectFileTypeDD.setFixedSize(int(60 * self.widthScale), int(25 * self.heightScale))

        self.chooseFormatContainer.addWidget(chooseFileTypeLabel)
        self.chooseFormatContainer.addWidget(self.selectFileTypeDD)
        self.chooseFormatContainer.setAlignment(Qt.AlignmentFlag.AlignLeft)

        #Put the main layout together
        self.mainSection.addLayout(self.titleContainer)
        self.mainSection.addSpacerItem(QSpacerItem(0, int(50 * self.heightScale), QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed))
        self.mainSection.addLayout(self.urlContainer)
        self.mainSection.addSpacerItem(QSpacerItem(0, int(10 * self.heightScale), QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed))
        self.mainSection.addLayout(self.downloadBarContainer)
        self.mainSection.addLayout(self.downloadInfoLayout)
        self.mainSection.addSpacerItem(QSpacerItem(0, int(75 * self.heightScale), QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed))
        self.mainSection.addLayout(self.chooseFolderContainer)
        self.mainSection.addSpacerItem(QSpacerItem(0, int(10 * self.heightScale), QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed))
        self.mainSection.addLayout(self.chooseFormatContainer)
        self.mainSection.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignHCenter)

    #Create the area to host the thumbnail image of the video. Will also display information about the video description, and more depending on the library functionality.
    def createRightSection(self):
        #TODO: Create the widgets and layouts for this section. 
        self.rightSection = QVBoxLayout()

        self.rightTitleContainer = QHBoxLayout()
        self.imageContaniner = QHBoxLayout()
        self.videoDescriptionLayout = QVBoxLayout()
        
        currentVideoLabel = QLabel("Video Information")
        currentVideoFont = QFont()
        currentVideoFont.setPointSize(20)
        currentVideoLabel.setFont(currentVideoFont)

        self.rightTitleContainer.addWidget(currentVideoLabel)
        self.rightTitleContainer.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        
        self.thumbnailContainer = QLabel()

        self.imageContaniner.addWidget(self.thumbnailContainer)

        self.videoDescription = QLabel()
        descriptionFont = QFont()
        descriptionFont.setPointSize(12)
        self.videoDescription.setFont(descriptionFont)

        self.videoDescriptionLayout.addWidget(self.videoDescription)

        self.rightSection.addSpacerItem(QSpacerItem(0, int(100 * self.heightScale), QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed))
        self.rightSection.addLayout(self.rightTitleContainer)
        self.rightSection.addLayout(self.imageContaniner)
        self.rightSection.addLayout(self.videoDescriptionLayout)
        self.rightSection.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignHCenter)

    #Combine all previous layouts and set the main window's central widget to be a QWidget object with it's layout set to the combined layout.
    def __init__(self):
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
        self.mainLayout.addLayout(self.mainSection)
        self.mainLayout.addLayout(self.rightSection)

        centralWidget = QWidget()
        centralWidget.setLayout(self.mainLayout)

        self.setCentralWidget(centralWidget)

    #Load in a thumbnail picture
    
    #------------------------
    #Start-up Functions
    #------------------------

    #Fill the output folder line edit widget 
    def fillOutputFolderDisplay(self):
        #Start by getting the file path of the config file
        configFilePath = os.path.join(os.path.dirname(__file__), 'defaultFolder.txt')

        #Read data from the file
        with open(configFilePath, 'r') as file:
            outputPath = file.readline()

        #Check if the config file has a path
        if outputPath:
            #Check if the path written still exists
            if os.path.exists(outputPath):
                self.selectFolderInput.setText(outputPath)
            
            else:
                #Just opens file in write mode, effectively clearing it of all data
                with open(configFilePath, 'w'):
                    pass
            
    #Get the names of all videos inside the current output folder, and list them under current videos
    def fillCurrentVideos(self):
        pass

    #------------------------
    #Slot Functions
    #------------------------

    #Choose New Output Folder
    def chooseOutputFolder(self):
        folder = self.openFolderDialog()
        if folder:
            self.selectFolderInput.setText(folder)
            
            configFilePath = os.path.join(os.path.dirname(__file__), 'defaultFolder.txt')
            with open(configFilePath, 'w') as file:
                file.write(folder)

    #Download a video using the URL
    def downloadVideo(self):
        try:        
            url = self.urlInput.text()
            yt = YouTube(url)
            stream = yt.streams.get_highest_resolution()
        except:
            self.urlInput.setText('')
            self.openStandardDialog('Error', 'Please enter a valid youtube URL.')
            return None
        
        #Set the thumbnail picture under the current video tab
        videoThumbnail = QPixmap()

        sampleUrl = yt.thumbnail_url
        urlResponse = urllib.request.urlopen(sampleUrl).read()
        videoThumbnail.loadFromData(urlResponse)
        videoThumbnail.setDevicePixelRatio(1.75)

        self.thumbnailContainer.setPixmap(videoThumbnail)

        #Add a description beneath the video thumbnail
        ytDescription = yt.description
        self.videoDescription.setText(ytDescription)
    
    #------------------------
    #Dialog Functions
    #------------------------

    #Open a standard message dialog
    def openStandardDialog(self, title, message):
        standardDialog = QDialog(self)
        standardDialog.setWindowTitle(title)
        
        dialogLayout = QVBoxLayout()
        okButton = QDialogButtonBox.StandardButton.Ok
        currentBtnBox = QDialogButtonBox(okButton)
        currentBtnBox.accepted.connect(standardDialog.accept)
        currentBtnBox.rejected.connect(standardDialog.reject)
        
        dialogMessage = QLabel(message)
        dialogMessage.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        dialogLayout.addWidget(dialogMessage)
        
        hbox = QHBoxLayout()
        hbox.addStretch(1)
        hbox.addWidget(currentBtnBox)
        hbox.addStretch(1)
        
        dialogLayout.addLayout(hbox)
        standardDialog.setLayout(dialogLayout)
        
        standardDialog.exec()

    #Prompts the user for a file, and returns the path to the file. Optional to add a mask for certain file types, and to start in a specific folder
    def openFileDialog(self, startingFolder = None, mask=None):
        pass

    #Prompts the user for a folder, and returns the path to the folder. Optional to start in a specific place
    def openFolderDialog(self, startingFolder = None):
        folder = QFileDialog().getExistingDirectory(self, 'Select Folder', '')
        return folder


#Main Function. Creates the Application
if __name__ == "__main__":
    app = QApplication([])

    window = MainWindow()
    window.show()
    
    app.exec()