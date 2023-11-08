#The purpose of this file will be to download youtube videos, when giving a video URL.

#Import Modules
import guiConstants
import os
import urllib.request
from DownloadThread import Downloader
from pytube import YouTube
from videoQueue import Queue

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


#Decorators
def checkOutputFolder(f):
        #Wrapper method
    def wrapper(*args, **kwargs):
        folderConfigPath = os.path.join(os.path.dirname(__file__), 'defaultFolder.txt')
        with open(folderConfigPath, 'r') as file:
            videoFolderPath = file.readline()

        #Check if path was set and exists
        if videoFolderPath:
            if os.path.exists(videoFolderPath):
                result = f(*args, **kwargs)
                return result
            else:
                #Reset Config File
                with open(videoFolderPath, 'w'):
                    pass
                
                return None
        else:
            return None

    return wrapper

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

        self.folderLabelFont = QFont()
        self.folderLabelFont.setPointSize(14)
        self.folderLabelFont.setBold(True)

        self.videoTreeStorage = []
        
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
        self.queueContainer = QVBoxLayout()
        
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
        self.fileTypeOptions = ['.mp4', '.mov', 'mkv', '.flv']
        self.selectFileTypeDD.addItems(self.fileTypeOptions)
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

        #Queue Videos Section
        self.queueInputSection = QHBoxLayout()
        self.allQueueItemsContainer = QVBoxLayout()

        #Section Title Label
        queueTitleLabel = QLabel("Add Video to Download Queue")
        queueTitleFont = QFont()
        queueTitleFont.setPointSize(18)
        queueTitleFont.setUnderline(True)
        queueTitleLabel.setFont(queueTitleFont)
        queueTitleLabel.setAlignment(Qt.AlignmentFlag.AlignHCenter)

        #Actual URL Input section
        queueInputLabel = QLabel("Video URL")
        queueInputLabel.setFont(urlFont)

        self.queueUrlInput = QLineEdit()
        self.queueUrlInput.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        self.queueUrlInput.setFixedWidth(int(250 * self.widthScale))

        self.addUrlButton = QPushButton("Add")
        self.addUrlButton.clicked.connect(self.addToQue)

        self.startQueueDownloadButton = QPushButton("Start")
        self.startQueueDownloadButton.clicked.connect(self.startQueueDownload)

        self.queueInputSection.addWidget(queueInputLabel)
        self.queueInputSection.addWidget(self.queueUrlInput)
        self.queueInputSection.addWidget(self.addUrlButton)
        self.queueInputSection.addSpacerItem(QSpacerItem(int(100 * self.widthScale), 0, QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Minimum))
        self.queueInputSection.addWidget(self.startQueueDownloadButton)

        self.queueContainer.addWidget(queueTitleLabel)
        self.queueContainer.addSpacerItem(QSpacerItem(0, int(50 * self.widthScale), QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed))
        self.queueContainer.addLayout(self.queueInputSection)
        self.queueContainer.addSpacerItem(QSpacerItem(0, int(25 * self.widthScale), QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed))

        #Video Queue Variables
        self.videoQueue = Queue()
        self.removeButtonSignals = []
        self.isQueue = False

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
        self.mainSection.addSpacerItem(QSpacerItem(0, int(10 * self.heightScale), QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed))
        self.mainSection.addLayout(self.queueContainer)
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

        #Call Set-up Functions
        self.fillOutputFolderDisplay()
        self.fillCurrentVideos()

        #Create the downloader thread
        self.downloadThread = Downloader()
        
        #Connect Signals
        self.downloadThread.videoInformationSignal.connect(self.loadVideoInformation)
        self.downloadThread.downloadInfo.connect(self.updateDownloadInfo)
        self.downloadThread.invalidUrlSignal.connect(self.invalidUrl)
        self.downloadThread.downloadProgressSignal.connect(self.updateProgressBar)
        self.downloadThread.downloadCompleteSignal.connect(self.downloadDone)

    
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

        self.fillCurrentVideos()
            
    #Get the names of all videos inside the current output folder, and list them under current videos
    @checkOutputFolder
    def fillCurrentVideos(self):
        #Check if the layout has the old video labels
        if len(self.videoTreeStorage) > 0:
            for i in range(len(self.videoTreeStorage)):
                self.videoNameContainer.removeWidget(self.videoTreeStorage[i])
        
        #Get path to video output folder
        videoFolderPath = self.selectFolderInput.text()
        self.videoTreeStorage = []
        
        folderItems = videoFolderPath.split('/')
        mainFolderName = folderItems[-1]
        mainFolderLabel = QLabel(mainFolderName)
        mainFolderLabel.setFont(self.folderLabelFont)

        self.videoNameContainer.addWidget(mainFolderLabel)
        self.videoTreeStorage.append(mainFolderLabel)

        self.displayFiles(videoFolderPath, 0)

    #Display all video files in a folder
    def displayFiles(self, folder, indentation):
        #Get all items in the folder
        allItems = os.listdir(folder)
        for item in allItems:
            #Get the path of the file or folder within the original folder
            itemPath = os.path.join(folder, item)
            if os.path.isfile(itemPath):
                #Isolate video title and file extension
                itemParts = item.split('.')
                
                #Check if the file is a video type
                fileExtension = '.' + itemParts[1]
                if fileExtension in self.fileTypeOptions:
                    #Add the title to the tree
                    currentVidTitle = itemParts[0]
                    if len(currentVidTitle) > 40:
                        currentVidTitle = currentVidTitle[0:38] + '...'
                    
                    #Temporary Visual of Spacing
                    currentVidTitle = ('    ' * (indentation + 1)) + currentVidTitle

                    #Create Label and add it to the layout
                    currentVideoLabel = QLabel(currentVidTitle)
                    currentVideoLabel.setFont(self.videoLabelFont)

                    self.videoNameContainer.addWidget(currentVideoLabel) 
                    self.videoTreeStorage.append(currentVideoLabel)

            if os.path.isdir(itemPath):
                #Call this function recursively, and increase indentation
                if os.path.getsize(itemPath) <= 0:
                    #Folder Exists but is empty, just move on
                    pass
                
                #folderParts = itemPath.split('/')
                folderParts = os.path.split(itemPath) 
                folderText = ('    ' * (indentation + 1)) + folderParts[-1]
                
                currentFolderLabel = QLabel(folderText)
                currentFolderLabel.setFont(self.folderLabelFont)

                self.videoNameContainer.addWidget(currentFolderLabel)
                self.videoTreeStorage.append(currentFolderLabel)

                self.displayFiles(itemPath, indentation + 1)


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

            self.fillCurrentVideos()

    #Download a video using the URL
    @checkOutputFolder
    def downloadVideo(self, *args, **kwargs):
        self.downloadInfoLabel.setText('Processing Video Info...')
        
        url = self.urlInput.text()
        self.downloadThread.setURL(url)
        self.urlInput.setText('')

        outputRes = self.resDD.currentText()
        self.downloadThread.setVideoRes(outputRes)

        outputDirectory = self.selectFolderInput.text()
        self.downloadThread.setOutputPath(outputDirectory)
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
        if percentDone < 10:
            totalWidth = 550
        elif 10 < percentDone < 99:
            totalWidth = 540
        else:
            totalWidth = 530

        progressText = "Progress {:.1f}%".format(percentDone) 
        self.progressBarLabel.setText(progressText)

        percentDecimal = percentDone / 100
        widthDone = int((totalWidth * percentDecimal) * self.widthScale)
        widthToGo = (totalWidth - widthDone) + 1
        if widthToGo <= 1:
            widthToGo = 0

        self.progressBarComplete.setFixedSize(widthDone, int(30 * self.heightScale))    
        self.progressBarIncomplete.setFixedSize(widthToGo, int(30 * self.heightScale))

    #Download is finished, move on to next video in Queue (if nec) and update visuals
    def downloadDone(self, type):
        #TODO Play a short audio indicating the downloading is done
        #If the video is part of a queue, check the download type. If type == 1, then it is either strictly audio or video, and it will wait for the type 2 to be emitted from the mend streams method.
        if self.isQueue:
            if type == 0 or type == 2:
                self.downloadNextVideo()
        else:
            #Play audio indicating download completed
            pass
        
        self.fillOutputFolderDisplay()


    
    #Add a video to the queue
    def addToQue(self):
        try:        
            url = self.queueUrlInput.text()
            yt = YouTube(url)
            #Clear the input field, regardless if text passed in was a video URL or not.
            self.queueUrlInput.setText('')
        except:
            self.queueUrlInput.setText('')
            self.openStandardDialog('Error', 'URL not valid.')
            return None

        queueItemLayout = QHBoxLayout()
        
        vidTitle = '    - ' + yt.title
        if len(vidTitle) > 50:
            vidTitle = vidTitle[:48] + '...'

        queueVidTitleLabel = QLabel(vidTitle)
        font = QFont()
        font.setPointSize(14)
        queueVidTitleLabel.setFont(font)
        
        removeItemButton = QPushButton('-')
        removeItemButton.setFixedSize(30, 30)
        removeItemButton.setStyleSheet(guiConstants.QUEUEBUTTONSTYLE)

        queueItemLayout.addWidget(queueVidTitleLabel)
        queueItemLayout.addWidget(removeItemButton)
        queueItemLayout.setAlignment(Qt.AlignmentFlag.AlignLeft)

        didQueue = self.videoQueue.enqueue(url, queueVidTitleLabel, removeItemButton, queueItemLayout)
        if not didQueue:
            #Delete Widgets from Memory
            queueVidTitleLabel.deleteLater()
            removeItemButton.deleteLater()
            queueItemLayout.deleteLater()

            #Relay Message to User that video has been added already
            self.openStandardDialog('Error', 'The video URL provided has already been added to the video download queue.')
            return None

        self.queueContainer.addLayout(queueItemLayout)
        
        self.updateButtonSignals()

    #Update the remove button signals, correctly linking each one to its corresponding index
    def updateButtonSignals(self):
        #Clear Prior Signals
        for connection in self.removeButtonSignals:
            connection[0].disconnect()

        #Reset Signal List
        self.removeButtonSignals = []

        #Loop through remove queue item button array, create a new signal for that button based on index, connect signal to the removeQueueItem method, 
        for i in range(self.videoQueue.getLength()):
            removeFunc = lambda checked, x=i: self.removeQueueItem(x, checked)
            button = self.videoQueue.videoQueue[i].getRemoveButton()
            buttonConnection = [button.clicked, removeFunc]
            buttonConnection[0].connect(buttonConnection[1])
            self.removeButtonSignals.append(buttonConnection)

    #Remove an item from the queue
    def removeQueueItem(self, item, checked):
        self.videoQueue.removeItem(item)
        self.updateButtonSignals()

    #Start the que download process
    @checkOutputFolder
    def startQueueDownload(self, *args, **kwargs):
        #First check if the queue has any videos at all.
        if self.videoQueue.isEmpty():
            self.openStandardDialog('Error', 'No videos were added to the download queue.')
            return None
        
        #Set Queue Flag to True to indicate downloaded videos are part of a queue, and disable main URL input to avoid errors
        self.isQueue = True
        self.urlInput.setReadOnly(True)
        self.startQueueDownloadButton.setEnabled(False)

        self.downloadNextVideo()

    #Run next queue item
    def downloadNextVideo(self):
        if self.videoQueue.isEmpty():
            self.isQueue = False
            self.urlInput.setReadOnly(False)
            self.startQueueDownloadButton.setEnabled(True)

            #TODO: Replace this with a pygame audio noise
            self.openStandardDialog('Success!', 'All videos queued for download have been successfully retrieved.')
            return None

        #Get the first item in the queue
        queueItem = self.videoQueue.dequeue()
        
        #Remove the widgets, and update the button signals
        queueItem.delWidgets()
        self.updateButtonSignals()

        #Set the Main URL Input text
        self.urlInput.setText(queueItem.getURL())
        
        #Download the video
        self.downloadVideo()

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