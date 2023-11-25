#This file will be the main app for the Quizlet match game 

#Imports
import logging
import os
from PyQt6.QtWidgets import (
    QMainWindow, QApplication, QLineEdit,
    QLabel, QPushButton, QDialog,
    QHBoxLayout, QVBoxLayout, QTabWidget,
    QGridLayout, QSizePolicy, QWidget,
    QSpacerItem
)
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QGuiApplication, QFont

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
        self.playMatchTab = QPushButton("Match")
        
        buttonSizes = QSize(int(150 * self.widthScale), int(75 * self.heightScale))
        
        self.createSetButton.setFixedSize(buttonSizes)
        self.playMatchTab.setFixedSize(buttonSizes)
        
        self.titleBarLayout.addWidget(self.createSetButton)
        self.titleBarLayout.addWidget(self.playMatchTab)
        self.titleBarLayout.setAlignment(Qt.AlignmentFlag.AlignLeft)
        
        self.logger.debug('Navigation bar complete.')
    
    #Create side bar for showing sets
    def createSideBar(self):
        self.logger.debug('Creating side bar...')
        self.sideBarLayout = QVBoxLayout()
        
        sideBarLabel = QLabel("Your Sets")
        sideBarFont = QFont()
        sideBarFont.setPointSize(24)
        sideBarLabel.setFont(sideBarFont)
        
        self.sideBarLayout.addWidget(sideBarLabel)
        self.logger.debug('Side bar complete.')
        
    
    #Create set tab
    def createSetTab(self):
        self.logger.debug('Creating new set area...')
        self.createSetLayout = QVBoxLayout()
        
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
        
        self.addPairLayout.addWidget(self.addPairButton)
        self.addPairLayout.setAlignment(Qt.AlignmentFlag.AlignRight)
        
        self.createSetLayout.addLayout(self.addPairLayout)
        
        self.logger.debug('New set area complete.')
        
    #Match tab for testing out sets
    def createMatchTab(self):
        pass
    
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
        
        self.completeLayout = QHBoxLayout()
        self.mainAreaLayout = QVBoxLayout()
        
        self.mainAreaLayout.addLayout(self.titleBarLayout)
        self.mainAreaLayout.addLayout(self.createSetLayout)
        
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
    
    #----------------------
    # Slot Functions
    #----------------------
    
    #Add a new term-definition pair in a new set
    def addSetPair(self):
        pass
        
#Main Method
if __name__ == "__main__":
    app = QApplication([])
    
    window = MainWindow()
    window.show()
    
    app.exec()