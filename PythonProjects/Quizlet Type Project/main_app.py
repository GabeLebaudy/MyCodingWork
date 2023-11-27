#This file will be the main app for the Quizlet match game 

#Imports
import logging
import os
from PyQt6.QtWidgets import (
    QMainWindow, QApplication, QLineEdit,
    QLabel, QPushButton, QDialog,
    QHBoxLayout, QVBoxLayout, QTabWidget,
    QGridLayout, QSizePolicy, QWidget,
    QSpacerItem, QTextEdit, QComboBox
)
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QGuiApplication, QFont
from set_obj import Set

#Main Window Class
class MainWindow(QMainWindow):
    #Initiate Log Method
    def initLogger(self):
        log_path = os.path.join(os.path.dirname(__file__), 'log_file.log')
        self.logger = logging.getLogger('Advanced Logging')
        self.logger.setLevel(logging.DEBUG)

        output = logging.FileHandler(log_path, 'w')
        formatter = logging.Formatter('%(name)s: %(levelname)s - %(message)s - %(asctime)s', 'on %m/%d/%Y at %H:%M %p')
        output.setFormatter(formatter)

        self.logger.addHandler(output)
    
    #Create title bar
    def createTitleBar(self):
        self.logger.debug('Creating navigation layout...')
        self.titleBarLayout = QHBoxLayout()
        
        self.createSetButton = QPushButton("Create Set")
        self.playMatchButton = QPushButton("Match")
        
        buttonSizes = QSize(int(150 * self.widthScale), int(75 * self.heightScale))
        
        self.createSetButton.setFixedSize(buttonSizes)
        self.createSetButton.clicked.connect(self.navCreateSet)
        
        self.playMatchButton.setFixedSize(buttonSizes)
        self.playMatchButton.clicked.connect(self.navMatch)
        
        self.titleBarLayout.addWidget(self.createSetButton)
        self.titleBarLayout.addWidget(self.playMatchButton)
        self.titleBarLayout.setAlignment(Qt.AlignmentFlag.AlignLeft)
        
        self.logger.debug('Navigation bar complete.')
    
    #Create side bar for showing sets
    def createSideBar(self):
        self.logger.debug('Creating side bar...')
        self.sideBarLayout = QVBoxLayout()
        
        self.sideBarLabel = QLabel("Your Sets")
        sideBarFont = QFont()
        sideBarFont.setPointSize(24)
        self.sideBarLabel.setFont(sideBarFont)
        
        self.sideBarLayout.addWidget(self.sideBarLabel)
        self.sideBarLayout.setAlignment(Qt.AlignmentFlag.AlignTop)
        
        self.logger.debug('Side bar complete.')
        
    #Create set tab
    def createSetTab(self):
        self.logger.debug('Creating new set area...')
        self.createSetContainer = QWidget()
        self.createSetLayout = QVBoxLayout()
        self.currentSet = Set()
        
        self.setLabelLayout = QHBoxLayout()
        termLabel = QLabel('Terms')
        definitionLabel = QLabel('Definitions')
        
        self.setLabelLayout.addWidget(termLabel)
        self.setLabelLayout.addWidget(definitionLabel)
        self.setLabelLayout.setAlignment(Qt.AlignmentFlag.AlignLeft)
        
        self.createSetLayout.addLayout(self.setLabelLayout)
        
        for i in range(5):
            self.addSetPair()
            
        self.addPairLayout = QHBoxLayout()
        
        self.addPairButton = QPushButton('+')
        self.addPairButton.setFixedSize(int(50 * self.widthScale), int(25 * self.heightScale))
        self.addPairButton.clicked.connect(self.addSetPair)
        
        self.addPairLayout.addWidget(self.addPairButton)
        self.addPairLayout.setAlignment(Qt.AlignmentFlag.AlignRight)
        
        self.createSetLayout.addLayout(self.addPairLayout)
        self.createSetContainer.setLayout(self.createSetLayout)
        
        self.logger.debug('New set area complete.')
        
    #Match tab for testing out sets
    def createMatchTab(self):
        self.logger.debug('Creating Match Tab...')
        
        self.matchContainer = QWidget()
        self.matchMainLayout = QVBoxLayout()

        matchLabel = QLabel("Match!")
        matchFont = QFont()
        matchFont.setPointSize(18)
        matchLabel.setFont(matchFont)

        self.startMatchLayout = QHBoxLayout()

        #Create the options for selecting a set to study
        self.selectSetDD = QComboBox()
        self.populateMatchDD()

        self.matchOptionsDD = QComboBox()
        matchOptions = ['Given Definition, Match Term', 'Given Term, Match Definition', 'Mixed']
        self.matchOptionsDD.addItems(matchOptions)

        self.startMatchButton = QPushButton('Start')
        
        self.startMatchLayout.addWidget(self.selectSetDD)
        self.startMatchLayout.addWidget(self.matchOptionsDD)
        self.startMatchLayout.addWidget(self.startMatchButton)
        self.startMatchLayout.setAlignment(Qt.AlignmentFlag.AlignHCenter)

        self.matchMainLayout.addWidget(matchLabel)
        self.matchMainLayout.addLayout(self.startMatchLayout)
        self.matchMainLayout.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignHCenter)
        self.matchContainer.setLayout(self.matchMainLayout)
        self.matchContainer.setHidden(True)
        
        self.logger.debug('Match tab complete.')

    #Main Window Construction
    def __init__(self):
        #Calls parent constructor to create the window
        self.initLogger()
        self.logger.debug('Initiating Window')
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
        
        self.createTitleBar()
        self.createSideBar()
        self.createSetTab()
        self.createMatchTab()

        self.completeLayout = QHBoxLayout()
        self.mainAreaLayout = QVBoxLayout()
        
        self.mainAreaLayout.addLayout(self.titleBarLayout)
        self.mainAreaLayout.addWidget(self.createSetContainer)
        self.mainAreaLayout.addWidget(self.matchContainer)
        
        self.completeLayout.addSpacerItem(QSpacerItem(int(25 * self.widthScale), 0, QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Minimum))
        self.completeLayout.addLayout(self.sideBarLayout)
        self.completeLayout.addSpacerItem(QSpacerItem(int(50 * self.widthScale), 0, QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Minimum))
        self.completeLayout.addLayout(self.mainAreaLayout)
        self.completeLayout.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft)
        
        centralWidget = QWidget()
        centralWidget.setLayout(self.completeLayout)
        self.setCentralWidget(centralWidget)
        
        self.logger.debug('Main window created.')
        
        
    #----------------------
    # Start-up Functions
    #----------------------
    
    #Populate the select set dropdown menu in the match tab
    def populateMatchDD(self):
        pass

    #----------------------
    # Slot Functions
    #----------------------
    
    #Go to Create Set Tab
    def navCreateSet(self):
        self.matchContainer.setHidden(True)
        self.createSetContainer.setHidden(False)
        

    #Go to Match Tab
    def navMatch(self):
        self.createSetContainer.setHidden(True)
        self.matchContainer.setHidden(False)

    #Add a new term-definition pair in a new set
    def addSetPair(self):
        pairLayout = QHBoxLayout()
        termInput = QTextEdit()
        definitionInput = QTextEdit()
        removeBtn = QPushButton('-')

        termInput.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Preferred)
        termInput.setFixedSize(int(500 * self.widthScale), int(25 * self.heightScale))

        definitionInput.setFixedSize(int(500 * self.widthScale), int(25 * self.heightScale))
        definitionInput.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Preferred)

        pairLayout.addWidget(termInput)
        pairLayout.addWidget(definitionInput)
        pairLayout.addWidget(removeBtn)
        
        self.currentSet.addNode(termInput, definitionInput, pairLayout, removeBtn)
        
        self.createSetLayout.addLayout(pairLayout)
        
        
        
#Main Method
if __name__ == "__main__":
    app = QApplication([])
    
    window = MainWindow()
    window.show()
    
    app.exec()