#This file will be used for the flashcards segment of quizlet

#Imports 
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QPushButton, QSpacerItem,
    QSizePolicy, QComboBox
)
from PyQt6.QtGui import QFont, QGuiApplication
from PyQt6.QtCore import Qt, QSize
from decorators import log_start_and_stop
import os
import logging
import random

#Logging Setup
LOGGER = logging.getLogger('Main Logger')
#Filepath to set information file
SETS_CONFIG_PATH = os.path.join(os.path.dirname(__file__), 'sets_configs.txt')

#Flashcards class
class FlashCards:
    #Constructor
    def __init__(self):
        #Get Scales
        screen_resolution = QGuiApplication.primaryScreen().availableGeometry()
        width, height = screen_resolution.width(), screen_resolution.height()
        self.widthScale = width / 1920
        self.heightScale = height / 1032
        
        #Where all layouts combine to
        self.flashcardsContainer = QWidget()
        self.containerLayout = QHBoxLayout()
        self.flashCardsMainLayout = QVBoxLayout()
        
        #Title Layout
        self.titleLayout = QHBoxLayout()
        
        titleLabel = QLabel('Flash Cards')
        titleFont = QFont()
        titleFont.setPointSize(24)
        titleFont.setBold(True)
        titleLabel.setFont(titleFont)
        
        self.titleLayout.addWidget(titleLabel)
        self.titleLayout.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        
        #Start Flash cards layout
        self.fcOptionsContainer = QWidget()
        self.fcOptionsLayout = QHBoxLayout()
        
        self.selectSetDD = QComboBox()
        self.directionDD = QComboBox()
        self.startGameBtn = QPushButton('Start')
        
        self.populateSetDD()
        self.directionDD.addItems(['Given Definition', 'Given Term', 'Mixed'])
        self.startGameBtn.clicked.connect(self.startGame)
        
        self.fcOptionsLayout.addWidget(self.selectSetDD)
        self.fcOptionsLayout.addWidget(self.directionDD)
        self.fcOptionsLayout.addWidget(self.startGameBtn)
        self.fcOptionsLayout.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        self.fcOptionsContainer.setLayout(self.fcOptionsLayout)
        
        #Main Game Layout
        self.mainGameContainer = QWidget()
        self.mainGameLayout = QVBoxLayout()
        self.flashCardLayout = QHBoxLayout()
        self.flashCardControlsLayout = QHBoxLayout()
        
        mainCardFont = QFont()
        mainCardFont.setPointSize(16)
        self.flashCardMainBtn = QPushButton()
        self.flashCardMainBtn.setFixedSize(int(750 * self.widthScale), int(500 * self.heightScale))
        self.flashCardMainBtn.setFont(mainCardFont)
        self.flashCardMainBtn.clicked.connect(self.flipCard)
        
        self.flashCardLayout.addWidget(self.flashCardMainBtn)
        self.flashCardLayout.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        
        self.previousBtn = QPushButton('Prev')
        self.nextBtn = QPushButton('Next')
        
        controlsButtonSize = QSize(int(100 * self.widthScale), int(40 * self.heightScale))
        
        self.previousBtn.setFixedSize(controlsButtonSize)
        self.nextBtn.setFixedSize(controlsButtonSize)
        
        self.previousBtn.clicked.connect(self.previousCard)
        self.nextBtn.clicked.connect(self.nextCard)
        
        self.flashCardControlsLayout.addWidget(self.previousBtn)
        self.flashCardControlsLayout.addStretch(1)
        self.flashCardControlsLayout.addWidget(self.nextBtn)
        self.flashCardControlsLayout.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        
        self.mainGameLayout.addLayout(self.flashCardLayout)
        self.mainGameLayout.addLayout(self.flashCardControlsLayout)
        self.mainGameLayout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.mainGameContainer.setLayout(self.mainGameLayout)
        self.mainGameContainer.setHidden(True)
        
        #Finished Game Layout
        self.finishedGameContainer = QWidget()
        self.finishedGameMainLayout = QVBoxLayout()
        self.messageLayout = QHBoxLayout()
        self.choiceControlsLayout = QHBoxLayout()
        
        finishedGameLabel = QLabel("Done! You've gone through all the pairs in this set.")
        finishedGameFont = QFont()
        finishedGameFont.setPointSize(14)
        finishedGameLabel.setFont(finishedGameFont)
        
        self.messageLayout.addWidget(finishedGameLabel)
        self.messageLayout.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        
        self.replaySetButton = QPushButton('Start Over')
        self.finishGameButton = QPushButton('Finish')
        
        self.replaySetButton.clicked.connect(self.replayCards)
        self.finishGameButton.clicked.connect(self.doneWithCards)
        
        self.choiceControlsLayout.addWidget(self.replaySetButton)
        self.choiceControlsLayout.addStretch(1)
        self.choiceControlsLayout.addWidget(self.finishGameButton)
        
        self.finishedGameMainLayout.addLayout(self.messageLayout)
        self.finishedGameMainLayout.addLayout(self.choiceControlsLayout)
        self.finishedGameMainLayout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.finishedGameContainer.setLayout(self.finishedGameMainLayout)
        self.finishedGameContainer.setHidden(True)
        
        #Combine into main layout
        self.flashCardsMainLayout.addLayout(self.titleLayout)
        self.flashCardsMainLayout.addSpacing(int(50 * self.heightScale))
        self.flashCardsMainLayout.addWidget(self.fcOptionsContainer)
        self.flashCardsMainLayout.addWidget(self.mainGameContainer)
        self.flashCardsMainLayout.addWidget(self.finishedGameContainer)
        self.flashCardsMainLayout.setAlignment(Qt.AlignmentFlag.AlignTop)
        
        self.containerLayout.addStretch(1)
        self.containerLayout.addLayout(self.flashCardsMainLayout)
        self.containerLayout.addStretch(1)
        
        self.flashcardsContainer.setLayout(self.containerLayout)
        self.flashcardsContainer.setHidden(True)
        
    #Get the Main Layout Container
    def getContainer(self):
        return self.flashcardsContainer
        
    #Show/Hide the layout
    def setHidden(self, status):
        self.flashcardsContainer.setHidden(status)
        
    #Add set names to dropdown menu
    @log_start_and_stop
    def populateSetDD(self):
        while self.selectSetDD.count() > 0:
            self.selectSetDD.removeItem(0)

        with open(SETS_CONFIG_PATH, 'r') as file:
            lines = file.readlines()

        for line in lines:
            line = line.rstrip()
            if ':' not in line:
                self.selectSetDD.addItem(line.rstrip())
    
    #Start Flash Cards Game
    def startGame(self):
        self.fcOptionsContainer.setHidden(True)
        self.mainGameContainer.setHidden(False)
        
        #Pull info about current set and mode
        self.currentSetName = self.selectSetDD.currentText()
        self.gamemode = self.directionDD.currentIndex()
        self.cardIndex = 0
        
        self.setData = []
        with open(SETS_CONFIG_PATH, 'r') as f:
            allData = f.readlines()
        
        flag = False
        for i in range(len(allData)):
            if flag:
                if ':' in allData[i].rstrip():
                    self.setData.append(allData[i].rstrip())
                else:
                    break
            if allData[i].rstrip() == self.currentSetName:
                flag = True
        
        self.shuffleData()
        self.loadCardData()
                
    #Shuffle all pairs in the data set
    def shuffleData(self):
        tempData = []
        while len(self.setData) > 0:
            index = random.randint(0, len(self.setData) - 1)
            tempData.append(self.setData[index])
            del self.setData[index]
            
        self.setData = tempData
            
    def loadCardData(self):
        #Check if Index is either the first or last card
        if self.cardIndex == 0:
            self.previousBtn.setEnabled(False)
        elif self.cardIndex == len(self.setData) - 1:
            self.nextBtn.setText('Finish')
        
        #Get front and back data
        frontText, backText = self.getCurrentCardData()
        self.cardData = [frontText, backText]
        
        self.flashCardMainBtn.setText(frontText)
        
    def getCurrentCardData(self):
        pair = self.setData[self.cardIndex]
        items = pair.split(':')
        if self.gamemode == 0:
            return items[1], items[0]  
        elif self.gamemode == 1:
            return items[0], items[1]
        else:
            front = random.randint(0, 1)
            if front == 0:
                back = 1
            else:
                back = 0
            
            return items[front], items[back]    
            
    #Flip the card over
    def flipCard(self):
        if self.cardData[0] == self.flashCardMainBtn.text():
            self.flashCardMainBtn.setText(self.cardData[1])
        else:
            self.flashCardMainBtn.setText(self.cardData[0])
            
    #Load Previous Card
    def previousCard(self):
        self.cardIndex -= 1
        if self.cardIndex == 0:
            self.previousBtn.setEnabled(False)
            
        if self.nextBtn.text() == 'Finish':
            self.nextBtn.setText('Next')
        
        self.loadCardData()
    
    #Load Next Card
    def nextCard(self):
        if not self.previousBtn.isEnabled():
            self.previousBtn.setEnabled(True)
        
        if self.cardIndex == len(self.setData) - 1:
            #Show Finish Screen
            self.finishCards()
            return
        
        self.cardIndex += 1
        self.loadCardData()
        
    #Last card is finished
    def finishCards(self):
        self.mainGameContainer.setHidden(True)
        self.finishedGameContainer.setHidden(False)
        self.nextBtn.setText('Next')
        
    #User chooses to replay the set
    def replayCards(self):
        self.shuffleData()
        self.cardIndex = 0
        
        self.finishedGameContainer.setHidden(True)
        self.mainGameContainer.setHidden(False)
        
        self.loadCardData()
    
    #User chooses to be done with flashcards
    def doneWithCards(self):
        self.mainGameContainer.setHidden(True)
        self.finishedGameContainer.setHidden(True)
        self.fcOptionsContainer.setHidden(False)
        
    
        