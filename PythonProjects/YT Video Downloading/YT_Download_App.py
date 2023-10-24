#The purpose of this file will be to download youtube videos, when giving a video URL.

#Import Modules
import guiConstants
import os
import urllib.request
from DownloadThread import Downloader

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
        self.videoNameContainer.setAlignment(Qt.AlignmentFlag.AlignLeft)

        #Create label for section
        allVideosLabel = QLabel("Current Videos")
        videoLabelFont = QFont()
        videoLabelFont.setPointSize(20)
        videoLabelFont.setUnderline(True)
        allVideosLabel.setFont(videoLabelFont)
        allVideosLabel.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        
        #Add all video names in the output folder to the layout
        self.videoLabelFont = QFont()
        self.videoLabelFont.setPointSize(14)

        self.fillCurrentVideos()
        
        #Put together layout
        self.leftSection.addSpacerItem(QSpacerItem(0, int(50 * self.heightScale), QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed))
        self.leftSection.addWidget(allVideosLabel)
        self.leftSection.addLayout(self.videoNameContainer)
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
        self.chooseResLayout = QHBoxLayout()
        
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
        self.urlContainer.setAlignment(Qt.AlignmentFlag.AlignLeft)

        #Download Bar Section: This section will display the current progress of the video download. 

        #TODO: Incorporate section for displaying that the file type is changing if that takes a signifigant portion of time to complete.
        self.progressBarLabel = QLabel("Progress: (0%)")
        self.progressBarLabel.setFont(urlFont)

        self.progressBarComplete = Color('#6ef246')
        self.progressBarIncomplete = Color('#4a4f48')

        self.progressBarComplete.setFixedSize(0, int(30 * self.heightScale))    
        self.progressBarIncomplete.setFixedSize(int(550 * self.widthScale), int(30 * self.heightScale))

        self.downloadBarContainer.addWidget(self.progressBarLabel)
        self.downloadBarContainer.addSpacerItem(QSpacerItem(int(10 * self.widthScale), 0, QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Minimum))
        self.downloadBarContainer.addWidget(self.progressBarComplete)
        self.downloadBarContainer.addWidget(self.progressBarIncomplete)
        self.downloadBarContainer.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.downloadBarContainer.setSpacing(0)

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
        self.chooseFolderContainer.setAlignment(Qt.AlignmentFlag.AlignLeft)

        #Choose File Type Section: This section will allow the user to choose the file extension if they want to switch from the default
        chooseFileTypeLabel = QLabel("File Type:")
        chooseFileTypeLabel.setFont(urlFont)

        #TODO: Make the text align to the right in the combo box
        self.selectFileTypeDD = QComboBox()
        fileTypeOptions = ['.mp4', '.wav']
        self.selectFileTypeDD.addItems(fileTypeOptions)
        self.selectFileTypeDD.setFixedSize(int(60 * self.widthScale), int(25 * self.heightScale))

        self.chooseFormatContainer.addWidget(chooseFileTypeLabel)
        self.chooseFormatContainer.addWidget(self.selectFileTypeDD)
        self.chooseFormatContainer.setAlignment(Qt.AlignmentFlag.AlignLeft)

        chooseResLabel = QLabel("Video Resolution:")
        chooseResLabel.setFont(urlFont)

        self.resDD = QComboBox()
        resOptions = ['1080p', '720p', '480p', '360p', '144p']
        self.resDD.addItems(resOptions)
        self.resDD.setFixedSize(int(60 * self.widthScale), int(25 * self.heightScale))

        self.chooseResLayout.addWidget(chooseResLabel)
        self.chooseResLayout.addWidget(self.resDD)
        self.chooseResLayout.setAlignment(Qt.AlignmentFlag.AlignLeft)

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
        self.mainSection.addLayout(self.chooseResLayout)
        self.mainSection.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignHCenter)

    #Create the area to host the thumbnail image of the video. Will also display information about the video description, and more depending on the library functionality.
    def createRightSection(self):
        self.rightSection = QVBoxLayout()

        self.rightTitleContainer = QHBoxLayout()
        self.vidTitleLayout = QHBoxLayout()
        self.imageContaniner = QHBoxLayout()
        self.videoDescriptionLayout = QVBoxLayout()
        self.videoDateLayout = QHBoxLayout()
        
        currentVideoLabel = QLabel("Video Information")
        currentVideoFont = QFont()
        currentVideoFont.setPointSize(20)
        currentVideoLabel.setFont(currentVideoFont)

        self.rightTitleContainer.addWidget(currentVideoLabel)
        self.rightTitleContainer.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        
        videoTitleLabel = QLabel("Title:")
        videoInfoLabelFont = QFont()
        videoInfoLabelFont.setPointSize(14)
        videoTitleLabel.setFont(videoInfoLabelFont)

        self.currentVideoTitle = QLabel()
        self.currentVideoTitle.setFont(videoInfoLabelFont)

        self.vidTitleLayout.addWidget(videoTitleLabel)
        self.vidTitleLayout.addWidget(self.currentVideoTitle)
        self.vidTitleLayout.setAlignment(Qt.AlignmentFlag.AlignLeft)

        self.thumbnailContainer = QLabel()
        thumbnailLabel = QLabel('Thumbnail:')
        thumbnailLabel.setFont(videoInfoLabelFont)
        thumbnailLabel.setAlignment(Qt.AlignmentFlag.AlignTop)

        self.imageContaniner.addWidget(thumbnailLabel)
        self.imageContaniner.addWidget(self.thumbnailContainer)
        self.imageContaniner.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft)

        descLabel = QLabel("Description:")
        descLabel.setFont(videoInfoLabelFont)

        self.videoDescription = QLabel()
        descriptionFont = QFont()
        descriptionFont.setPointSize(12)
        self.videoDescription.setFont(descriptionFont)
        self.videoDescription.setFixedWidth(int(500 * self.widthScale))
        self.videoDescription.setWordWrap(True)

        self.videoDescriptionLayout.addWidget(descLabel)
        self.videoDescriptionLayout.addWidget(self.videoDescription)
        self.videoDescriptionLayout.setAlignment(Qt.AlignmentFlag.AlignTop)

        dateLabel = QLabel("Publish Date:")
        dateLabel.setFont(videoInfoLabelFont)

        self.publishDateLabel = QLabel()
        self.publishDateLabel.setFont(videoInfoLabelFont)
        
        self.videoDateLayout.addWidget(dateLabel)
        self.videoDateLayout.addWidget(self.publishDateLabel)
        self.videoDateLayout.setAlignment(Qt.AlignmentFlag.AlignLeft)

        self.rightSection.addSpacerItem(QSpacerItem(0, int(50 * self.heightScale), QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed))
        self.rightSection.addLayout(self.rightTitleContainer)
        self.rightSection.addSpacerItem(QSpacerItem(0, int(10 * self.heightScale), QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed))
        self.rightSection.addLayout(self.vidTitleLayout)
        self.rightSection.addLayout(self.imageContaniner)
        self.rightSection.addLayout(self.videoDescriptionLayout)
        self.rightSection.addLayout(self.videoDateLayout)
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

        #Create the downloader thread
        self.downloadThread = Downloader()
        
        #Connect Signals
        self.downloadThread.videoInformationSignal.connect(self.loadVideoInformation)
        self.downloadThread.downloadInfo.connect(self.updateDownloadInfo)
        self.downloadThread.invalidUrlSignal.connect(self.invalidUrl)
        self.downloadThread.downloadProgressSignal.connect(self.updateProgressBar)
    
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
        #Get the path to the folder containing the videos
        folderConfigPath = os.path.join(os.path.dirname(__file__), 'defaultFolder.txt')
        with open(folderConfigPath, 'r') as file:
            videoFolderPath = file.readline()

        #Check if path was set and exists
        if videoFolderPath:
            if os.path.exists(videoFolderPath):
                pass
            else:
                #Reset Config File
                with open(videoFolderPath, 'w'):
                    pass
                return None
        else:
            return None
        
        self.displayFiles(videoFolderPath, 0)

    #Display all video files in a folder
    def displayFiles(self, folder, indentation):
        #Get all items in the folder
        allItems = os.listdir(folder)
        for item in allItems:
            #Get the path of the file or folder within the original folder
            itemPath = os.path.join(folder, item)
            if os.path.isfile(itemPath):
                #Get the title of the video without file extension
                itemParts = item.split('.')
                currentVidTitle = itemParts[0]
                if len(currentVidTitle) > 40:
                    currentVidTitle = currentVidTitle[0:38] + '...'
                
                #Create Label and add it to the layout
                currentVideoLabel = QLabel(currentVidTitle)
                currentVideoLabel.setFont(self.videoLabelFont)

                self.videoNameContainer.addWidget(currentVideoLabel) 

            if os.path.isdir(itemPath):
                #Call this function recursively, and increase indentation
                pass
            else:
                #Item is not a folder nor a file, just pass over it.
                pass


    #------------------------
    #Slot Functions
    #------------------------
    
    #- GUI Slots

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
        self.downloadInfoLabel.setText('Processing Video Info...')
        
        url = self.urlInput.text()
        self.downloadThread.setURL(url)

        outputDirectory = self.selectFolderInput.text()
        if outputDirectory:
            if os.path.exists(outputDirectory):
                self.downloadThread.setOutputPath(outputDirectory)
            else:
                self.openStandardDialog('Error', 'Please use a valid folder directory in your computer system.')
                return None
        else:
            self.openStandardDialog('Error', 'You must set the output folder directory before downloading videos.')
            return None
        
        self.downloadThread.start()

    #-Thread Slots
    
    #Load in video information
    def loadVideoInformation(self, videoInfo):
        #Video Title
        vidTitle = videoInfo[0]
        if len(vidTitle) >= 50:
            vidTitle = vidTitle[:48] + '...'

        self.currentVideoTitle.setText(vidTitle)

        #Video Thumbnail
        videoThumbnail = QPixmap()

        urlResponse = urllib.request.urlopen(videoInfo[1]).read()
        videoThumbnail.loadFromData(urlResponse)
        videoThumbnail.setDevicePixelRatio(1.75)

        self.thumbnailContainer.setPixmap(videoThumbnail)

        #Video Description
        self.videoDescription.setText(videoInfo[2])

        #Video Date 
        self.publishDateLabel.setText(videoInfo[3])

    #Update download info tracker
    def updateDownloadInfo(self, info):
        self.downloadInfoLabel.setText(info)

    #User entered an invalid URL
    def invalidUrl(self):
        self.urlInput.setText('')
        self.openStandardDialog('Error', 'Please enter a valid youtube URL.')

    #Update the Progress Bar
    def updateProgressBar(self, percentDone):
        progressText = "Progress {:.1f}%".format(percentDone) 
        self.progressBarLabel.setText(progressText)

        percentDecimal = percentDone / 100
        widthDone = int((550 * percentDecimal) * self.widthScale)
        widthToGo = (550 - widthDone) + 1
        if widthToGo <= 1:
            widthToGo = 0

        self.progressBarComplete.setFixedSize(widthDone, int(30 * self.heightScale))    
        self.progressBarIncomplete.setFixedSize(widthToGo, int(30 * self.heightScale))

    
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