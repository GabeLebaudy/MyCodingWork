#This file will be the main app for the Quizlet match game 

#Imports
import logging
import os
from PyQt6.QtWidgets import (
    QMainWindow, QApplication, QLineEdit,
    QLabel, QPushButton, QDialog,
    QHBoxLayout, QVBoxLayout, QTabWidget,
    QGridLayout, QSizePolicy, QWidget,
    QSpacerItem, QTextEdit, QComboBox,
    QDialogButtonBox
)
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QGuiApplication, QFont
from set_obj import Set
from sidebar import SideBar
from match import Match
from decorators import log_start_and_stop


#Logging Setup
LOGGER = logging.getLogger('Main Logger')

#Main Window Class
class MainWindow(QMainWindow):
    #Create title bar
    @log_start_and_stop
    def createTitleBar(self):
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
    
    #Create side bar for showing sets
    @log_start_and_stop
    def createSideBar(self):
        self.sideBarLayout = QVBoxLayout()
        self.sideBar = SideBar()
        
        sideBarLabel = QLabel("Your Sets")
        sideBarFont = QFont()
        sideBarFont.setPointSize(24)
        sideBarLabel.setFont(sideBarFont)
        
        self.sideBarLayout.addWidget(sideBarLabel)
        self.sideBarLayout.setAlignment(Qt.AlignmentFlag.AlignTop)
        
        self.sideBarLayout.addWidget(sideBarLabel)
        self.populateSideBar()
        
    #Create set tab
    @log_start_and_stop
    def createSetTab(self):
        self.set = Set()
        self.removePairSignals = []

        self.createSetContainer = QWidget()
        containerLayout = QHBoxLayout()
        self.createSetLayout = QVBoxLayout()
        
        self.setLabelLayout = QHBoxLayout()
        termLabel = QLabel('Terms')
        definitionLabel = QLabel('Definitions')

        createSetFont = QFont()
        createSetFont.setPointSize(16)
        createSetFont.setBold(True)

        termLabel.setFont(createSetFont)
        definitionLabel.setFont(createSetFont)
        
        self.setLabelLayout.addSpacerItem(QSpacerItem(int(215 * self.widthScale), 0, QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Minimum))
        self.setLabelLayout.addWidget(termLabel)
        self.setLabelLayout.addSpacerItem(QSpacerItem(int(420 * self.widthScale), 0, QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Minimum))
        self.setLabelLayout.addWidget(definitionLabel)
        self.setLabelLayout.setAlignment(Qt.AlignmentFlag.AlignLeft)
        
        self.createSetLayout.addLayout(self.setLabelLayout)
        
        self.itemPairsLayout = QVBoxLayout()
        for i in range(5):
            self.addSetPair()
            
        self.addPairLayout = QHBoxLayout()
        
        self.addPairButton = QPushButton('+')
        self.addPairButton.setFixedSize(int(75 * self.widthScale), int(40 * self.heightScale))
        self.addPairButton.clicked.connect(self.addSetPair)
        
        self.addPairLayout.addWidget(self.addPairButton)
        self.addPairLayout.setAlignment(Qt.AlignmentFlag.AlignRight)

        self.finishSetLayout = QHBoxLayout()

        self.finishSetButton = QPushButton("Create")
        self.finishSetButton.setFixedSize(int(125 * self.widthScale), int(50 * self.heightScale))
        self.finishSetButton.clicked.connect(self.finalizeSet)

        self.finishSetLayout.addWidget(self.finishSetButton)
        self.finishSetLayout.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        
        self.createSetLayout.addLayout(self.itemPairsLayout)
        self.createSetLayout.addSpacerItem(QSpacerItem(0, int(20 * self.heightScale), QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed))
        self.createSetLayout.addLayout(self.addPairLayout)
        self.createSetLayout.addLayout(self.finishSetLayout)
        self.createSetLayout.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignHCenter)

        containerLayout.addSpacerItem(QSpacerItem(0, 0, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum))
        containerLayout.addLayout(self.createSetLayout)
        containerLayout.addSpacerItem(QSpacerItem(0, 0, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum))
        self.createSetContainer.setLayout(containerLayout)
        
    #Match tab for testing out sets
    @log_start_and_stop
    def createMatchTab(self):
        self.match = Match()
        self.matchContainer = QWidget()
        self.matchMainLayout = QVBoxLayout()

        #Match home screen
        matchLabel = QLabel("Match!")
        matchFont = QFont()
        matchFont.setPointSize(24)
        matchLabel.setFont(matchFont)
        matchLabel.setAlignment(Qt.AlignmentFlag.AlignHCenter)

        self.startMatchLayout = QHBoxLayout()
        self.startMatchContainer = QWidget()

        #Create the options for selecting a set to study
        self.selectSetDD = QComboBox()
        self.populateMatchDD()

        self.matchOptionsDD = QComboBox()
        matchOptions = ['Given Definition, Match Term', 'Given Term, Match Definition', 'Mixed']
        self.matchOptionsDD.addItems(matchOptions)

        self.startMatchButton = QPushButton('Start')
        self.startMatchButton.clicked.connect(self.startMatch)
        
        self.startMatchLayout.addWidget(self.selectSetDD)
        self.startMatchLayout.addWidget(self.matchOptionsDD)
        self.startMatchLayout.addWidget(self.startMatchButton)
        self.startMatchLayout.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        self.startMatchContainer.setLayout(self.startMatchLayout)
        
        #Actual Match layout
        self.mainMatchQLayout = QVBoxLayout()
        self.mainMatchQContainer = QWidget()
        
        questionFont = QFont()
        questionFont.setPointSize(14)

        self.matchInfoLayout = QHBoxLayout()
        self.matchInfoLabel = QLabel('0/0')
        self.matchInfoLabel.setFont(questionFont)
        
        self.matchInfoLayout.addWidget(self.matchInfoLabel)
        self.matchInfoLayout.addSpacerItem(QSpacerItem(int(300 * self.widthScale), 0, QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Minimum))
        self.matchInfoLayout.setAlignment(Qt.AlignmentFlag.AlignRight)
        
        self.questionLayout = QHBoxLayout()
        self.questionLabel = QLabel('Sample Question')
        self.questionLabel.setFont(questionFont)
        
        self.questionLayout.addWidget(self.questionLabel)
        self.questionLayout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        self.answerLayout = QHBoxLayout() 
        self.answerInput = QLineEdit()
        self.submitAnswerBtn = QPushButton('Check')
        
        self.answerInput.returnPressed.connect(self.checkMatchAnswer)
        self.submitAnswerBtn.clicked.connect(self.checkMatchAnswer)
        
        answerFont = QFont()
        answerFont.setPointSize(16)
        self.answerInput.setFont(answerFont)
        self.answerInput.setFixedSize(int(500 * self.widthScale), int(40 * self.heightScale))
        self.answerInput.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Preferred)

        self.submitAnswerBtn.setFixedSize(int(100 * self.widthScale), int(40 * self.heightScale))
        self.submitAnswerBtn.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        
        self.answerLayout.addWidget(self.answerInput)
        self.answerLayout.addWidget(self.submitAnswerBtn)
        self.answerLayout.setAlignment(Qt.AlignmentFlag.AlignHCenter)

        #Combine Main Game Layout
        self.mainMatchQLayout.addLayout(self.matchInfoLayout)
        self.mainMatchQLayout.addLayout(self.questionLayout)
        self.mainMatchQLayout.addSpacerItem(QSpacerItem(0, int(25 * self.heightScale), QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed))
        self.mainMatchQLayout.addLayout(self.answerLayout)
        self.mainMatchQContainer.setLayout(self.mainMatchQLayout)
        self.mainMatchQContainer.setHidden(True)

        #Layout for correct answer
        self.answerCorrectLayout = QVBoxLayout()
        self.answerCorrectContainer = QWidget()
        
        answerCorrectLabel = QLabel('Correct!')
        answerCorrectFont = QFont()
        answerCorrectFont.setPointSize(24)
        answerCorrectLabel.setFont(answerCorrectFont)

        self.continueMatchBtn = QPushButton('Next')
        self.continueMatchBtn.setFixedSize(int(100 * self.widthScale), int(40 * self.heightScale))
        self.continueMatchBtn.clicked.connect(self.startNextMatchPair)

        self.answerCorrectLayout.addWidget(answerCorrectLabel)
        self.answerCorrectLayout.addSpacerItem(QSpacerItem(0, int(25 * self.heightScale), QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed))
        self.answerCorrectLayout.addWidget(self.continueMatchBtn)
        self.answerCorrectLayout.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        self.answerCorrectContainer.setLayout(self.answerCorrectLayout)
        self.answerCorrectContainer.setHidden(True)
        
        #Layout for incorrect answer
        self.incorrectAnswerContainer = QWidget()
        self.incorrectAnswerLayout = QVBoxLayout()

        incorrectAnswerLabel = QLabel('Incorrect')
        incorrectAnswerLabel.setFont(answerCorrectFont)

        self.answerDisplayLabel = QLabel('The correct answer was: ')
        self.answerDisplayLabel.setFont(answerFont)

        self.yourAnswerDisplayLabel = QLabel('Your answer was: ')
        self.yourAnswerDisplayLabel.setFont(answerFont)

        self.incorrectAnswerChoiceLayout = QHBoxLayout()
        self.overrideBtn = QPushButton('Override, I was right.')
        self.continueWithWrongAnswerBtn = QPushButton('Continue')

        self.overrideBtn.clicked.connect(self.overrideWrongAnswer)
        self.continueWithWrongAnswerBtn.clicked.connect(self.continueMatchWrong)

        self.incorrectAnswerChoiceLayout.addWidget(self.overrideBtn)
        self.incorrectAnswerChoiceLayout.addWidget(self.continueWithWrongAnswerBtn)
        self.incorrectAnswerChoiceLayout.setAlignment(Qt.AlignmentFlag.AlignHCenter)

        self.incorrectAnswerLayout.addWidget(incorrectAnswerLabel)
        self.incorrectAnswerLayout.addWidget(self.answerDisplayLabel)
        self.incorrectAnswerLayout.addWidget(self.yourAnswerDisplayLabel)
        self.incorrectAnswerLayout.addLayout(self.incorrectAnswerChoiceLayout)
        self.incorrectAnswerLayout.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        self.incorrectAnswerContainer.setLayout(self.incorrectAnswerLayout)
        self.incorrectAnswerContainer.setHidden(True)

        #Match completed screen
        self.matchCompletedContainer = QWidget()
        self.matchCompletedLayout = QVBoxLayout()

        matchCompletedLabel = QLabel('Good Job!')
        matchCompletedLabel.setFont(answerCorrectFont)

        self.matchCompletedBtnLayout = QHBoxLayout()

        self.replayMatchBtn = QPushButton('Replay set')
        self.finishMatchBtn = QPushButton('Finish')

        self.replayMatchBtn.clicked.connect(self.replayMatchGame)
        self.finishMatchBtn.clicked.connect(self.resetMatchTab)

        self.matchCompletedBtnLayout.addWidget(self.replayMatchBtn)
        self.matchCompletedBtnLayout.addWidget(self.finishMatchBtn)

        self.matchCompletedLayout.addWidget(matchCompletedLabel)
        self.matchCompletedLayout.addLayout(self.matchCompletedBtnLayout)
        self.matchCompletedLayout.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        self.matchCompletedContainer.setLayout(self.matchCompletedLayout)
        self.matchCompletedContainer.setHidden(True)

        #Container for all match layouts
        self.matchMainLayout.addSpacerItem(QSpacerItem(0, 0, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum))
        self.matchMainLayout.addWidget(matchLabel)
        self.matchMainLayout.addSpacerItem(QSpacerItem(0, int(50 * self.heightScale), QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed))
        self.matchMainLayout.addWidget(self.startMatchContainer)
        self.matchMainLayout.addWidget(self.mainMatchQContainer)
        self.matchMainLayout.addWidget(self.answerCorrectContainer)
        self.matchMainLayout.addWidget(self.incorrectAnswerContainer)
        self.matchMainLayout.addWidget(self.matchCompletedContainer)
        self.matchMainLayout.addSpacerItem(QSpacerItem(0, 0, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum))
        self.matchMainLayout.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignHCenter)
        self.matchContainer.setLayout(self.matchMainLayout)
        self.matchContainer.setHidden(True)

    #Main Window Construction
    @log_start_and_stop
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
        
        self.createTitleBar()
        self.createSideBar()
        self.createSetTab()
        self.createMatchTab()

        self.completeLayout = QHBoxLayout()
        self.mainAreaLayout = QVBoxLayout()
        
        self.mainAreaLayout.addLayout(self.titleBarLayout)
        self.mainAreaLayout.addSpacerItem(QSpacerItem(0, int(30 * self.heightScale), QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed))
        self.mainAreaLayout.addWidget(self.createSetContainer)
        self.mainAreaLayout.addWidget(self.matchContainer)
        self.mainAreaLayout.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        
        self.completeLayout.addSpacerItem(QSpacerItem(int(25 * self.widthScale), 0, QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Minimum))
        self.completeLayout.addLayout(self.sideBarLayout)
        self.completeLayout.addSpacerItem(QSpacerItem(int(50 * self.widthScale), 0, QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Minimum))
        self.completeLayout.addLayout(self.mainAreaLayout)
        self.completeLayout.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft)
        
        centralWidget = QWidget()
        centralWidget.setLayout(self.completeLayout)
        self.setCentralWidget(centralWidget)
        
        
    #----------------------
    # Start-up Functions
    #----------------------
    
    #Populate the Side Bar
    @log_start_and_stop
    def populateSideBar(self):
        setsConfigsPath = os.path.join(os.path.dirname(__file__), 'sets_configs.txt')
        with open(setsConfigsPath, 'r') as file:
            lines = file.readlines()

        for line in lines:
            line = line.rstrip()
            if ':' not in line:
                self.addSideBarSet(line)

    #Add a entry for a set on the side bar
    def addSideBarSet(self, title):
        setLayout = QHBoxLayout()
        titleLabel = QLabel(title)
        editBtn = QPushButton('Edit')
        deleteBtn = QPushButton('Delete')

        #TODO: Fix this word wrap issue
        titleLabel.setFixedWidth(int(125 * self.widthScale))
        titleLabel.setWordWrap(True)
                
        setLayout.addWidget(titleLabel)
        setLayout.addWidget(editBtn)
        setLayout.addWidget(deleteBtn)
        setLayout.setAlignment(Qt.AlignmentFlag.AlignLeft)
        
        self.sideBarLayout.addLayout(setLayout)
        self.sideBar.addNode(titleLabel, editBtn, deleteBtn, setLayout)
        
        #TODO: Work with edit and delete signals
    
    #Populate the select set dropdown menu in the match tab
    @log_start_and_stop
    def populateMatchDD(self):
        setsConfigsPath = os.path.join(os.path.dirname(__file__), 'sets_configs.txt')
        with open(setsConfigsPath, 'r') as file:
            lines = file.readlines()

        for line in lines:
            line = line.rstrip()
            if ':' not in line:
                self.selectSetDD.addItem(line.rstrip())

    #----------------------
    # Slot Functions
    #----------------------
    
    #Switch to create set tab
    def navCreateSet(self):
        self.matchContainer.setHidden(True)
        self.createSetContainer.setHidden(False)

    #Switch to match tab
    def navMatch(self):
        self.createSetContainer.setHidden(True)
        self.matchContainer.setHidden(False)

    #Add a new term-definition pair in a new set
    def addSetPair(self):
        pairLayout = QHBoxLayout()
        termInput = QTextEdit()
        defInput = QTextEdit()
        removeBtn = QPushButton('-')

        inputSize = QSize(int(500 * self.widthScale), int(50 * self.heightScale))
        termInput.setFixedSize(inputSize)
        defInput.setFixedSize(inputSize)
        
        termInput.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
        defInput.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)

        pairLayout.addWidget(termInput)
        pairLayout.addWidget(defInput)
        pairLayout.addWidget(removeBtn)
        pairLayout.setAlignment(Qt.AlignmentFlag.AlignHCenter)

        self.itemPairsLayout.addLayout(pairLayout)
        self.set.addNode(termInput, defInput, pairLayout, removeBtn)
        self.updatePairSignals()

    #Update the remove pair button signals
    def updatePairSignals(self):
        #Clear Prior Signals
        for connection in self.removePairSignals:
            connection[0].disconnect()

        #Reset Signal List
        self.removePairSignals = []

        #Loop through remove queue item button array, create a new signal for that button based on index, connect signal to the removeQueueItem method, 
        for i in range(self.set.getLength()):
            removeFunc = lambda checked, x=i: self.removeSetPair(x, checked)
            button = self.set.items[i].getBtn()
            buttonConnection = [button.clicked, removeFunc]
            buttonConnection[0].connect(buttonConnection[1])
            self.removePairSignals.append(buttonConnection)

    #Remove a pair from the set (Null is added so that index parameter won't get used by checked status of the button)
    def removeSetPair(self, index, null):
        self.set.removeNode(index)
        self.updatePairSignals()
    
    #Start the match game
    @log_start_and_stop
    def startMatch(self, *args, **kwargs):
        #Pull match parameters
        matchSet = self.selectSetDD.currentText()
        gamemode = self.matchOptionsDD.currentIndex()

        #Populate Match Storage
        configPath = os.path.join(os.path.dirname(__file__), 'sets_configs.txt')
        with open(configPath, 'r') as f:
            lines = f.readlines()

        startIndex = -1
        for i in range(len(lines)):
            if lines[i].rstrip() == matchSet:
                startIndex = i
                break 

        if startIndex == -1:
            self.openMessageDialog('Error', "The program couldn't find the set selected.")
            return 

        for i in range(startIndex + 1, len(lines)):
            lines[i] = lines[i].rstrip()
            if ':' in lines[i]:
                contents = lines[i].split(':')
                self.match.addMatchPair(contents[0], contents[1])
            else:
                break                
        
        #Set the match gamemode from input
        self.match.setGamemode(gamemode)
        
        #Shuffle the pairs
        self.match.shuffle()
        
        #Set match layout
        self.startMatchContainer.setHidden(True)
        self.mainMatchQContainer.setHidden(False)
        
        #Initialize progress label info
        self.lenFullSet = self.match.getLength()
        self.correctCounter = 0

        #Start game
        self.startNextMatchPair()
        
    #Give user the next match question
    def startNextMatchPair(self):
        #Show correct layout while hiding post-answer layouts
        self.answerCorrectContainer.setHidden(True)
        self.incorrectAnswerContainer.setHidden(True)
        self.mainMatchQContainer.setHidden(False)

        #Set the progress label text
        self.matchInfoLabel.setText('{}/{}'.format(self.correctCounter, self.lenFullSet))

        #Pull question text
        question = self.match.getQuestion()
        self.questionLabel.setText(question)
    
    #Check user inputted answer
    def checkMatchAnswer(self):
        #Check is the user entered anything
        if not self.answerInput.text():
            return
        
        #Pull answer then wipe input
        userAnswer = self.answerInput.text()
        self.answerInput.setText('')
        isCorrect, answer = self.match.isRight(userAnswer)

        #Check answer
        if isCorrect:
            self.correctCounter += 1
            self.match.answeredCorrect()

            #Check if answer was the last question
            if self.correctCounter >= self.lenFullSet:
                self.matchComlpeted()
                return
             
            #Answer was correct, show correct layout, with button linked to start the next question
            self.mainMatchQContainer.setHidden(True)
            self.answerCorrectContainer.setHidden(False)
        else:
            #Answer was incorrect, show incorrect answer layout, with a manual override, or continue button.
            self.mainMatchQContainer.setHidden(True)
            self.incorrectAnswerContainer.setHidden(False)

            #Show correct answer
            self.answerDisplayLabel.setText('The correct answer was: {}'.format(answer))
            self.yourAnswerDisplayLabel.setText('Your answer was: {}'.format(userAnswer))

    #Override incorrect answer
    def overrideWrongAnswer(self):
        #Act as if answer was correct
        self.correctCounter += 1
        self.match.answeredCorrect()

        #Check if answer was the last question
        if self.correctCounter >= self.lenFullSet:
            self.matchComlpeted()
            return
        
        #Continue with the game
        self.startNextMatchPair()


    #Continue with wrong answer
    def continueMatchWrong(self):
        self.match.reshuffleQuestion()
        self.startNextMatchPair()

    #Show finished match screen
    @log_start_and_stop
    def matchComlpeted(self):
        #Reset match object
        self.match.resetGame()

        #Show the match complete screen
        self.answerCorrectContainer.setHidden(True)
        self.incorrectAnswerContainer.setHidden(True)
        self.mainMatchQContainer.setHidden(True)
        self.matchCompletedContainer.setHidden(False)      

    #Replay set button   
    def replayMatchGame(self):
        self.matchCompletedContainer.setHidden(True)
        self.startMatch()

    #Reset match tab
    def resetMatchTab(self):
        self.matchCompletedContainer.setHidden(True)
        self.startMatchContainer.setHidden(False)

    #Finalize the creation of a new set
    @log_start_and_stop
    def finalizeSet(self, *args, **kwargs):
        emptyFlag = self.set.isPairsEmpty()

        if emptyFlag == 0:
            self.openMessageDialog('Error', 'At least one term is needed')
            return
        elif emptyFlag == 1:
            self.openMessageDialog('Error', 'At least one pair is incomplete')
            return
        
        #Prompt user for name for the set
        setName = self.textInputDialog('Dialog Title', 'Enter a name for this set:')

        configPath = os.path.join(os.path.dirname(__file__), 'sets_configs.txt')
        setVals = self.set.getPairData()
        with open(configPath, 'a') as file:
            title = '{}\n'.format(setName)
            file.write(title)
            for term in setVals:
                s = '{}:{}\n'.format(term, setVals[term])
                file.write(s)

        #Add title to dropdowns and side bar
        self.addSideBarSet(setName)
        self.selectSetDD.addItem(setName)
        
        #Ping user that set was successfully created
        self.openMessageDialog('Success!', 'Your set {} was successfully created!'.format(setName))
            
    #----------------------
    # Dialog Methods
    #----------------------
    
    #Standard message dialog
    def openMessageDialog(self, title, message):
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

    #Prompt user for input dialog
    def textInputDialog(self, title, prompt):
        titleDialog = QDialog(self)
        titleDialog.setWindowTitle(title)
        
        dialogLayout = QVBoxLayout()
        titleDialogLayout = QHBoxLayout()
        saveBtn = QDialogButtonBox.StandardButton.Save
        cancelBtn = QDialogButtonBox.StandardButton.Cancel
        titleButtonBox = QDialogButtonBox()
        
        titleButtonBox.addButton(saveBtn)
        titleButtonBox.addButton(cancelBtn)
        
        titleButtonBox.accepted.connect(titleDialog.accept)
        titleButtonBox.rejected.connect(titleDialog.reject)
        
        dialogMessage = QLabel(prompt)
        titleDialogInput = QLineEdit()
        dialogMessage.setAlignment(Qt.AlignmentFlag.AlignTop)
        titleDialogLayout.addWidget(dialogMessage)
        titleDialogLayout.addWidget(titleDialogInput)
        
        hbox = QHBoxLayout()
        hbox.addStretch(1)
        hbox.addWidget(titleButtonBox)
        
        dialogLayout.addLayout(titleDialogLayout)
        dialogLayout.addLayout(hbox)
        titleDialog.setLayout(dialogLayout)
        
        if titleDialog.exec() == QDialog.DialogCode.Accepted:
            # Retrieve the entered title from the input field
            response = titleDialogInput.text()
            
            return response
        else:
            return False
        
#Main Method
if __name__ == "__main__":
    app = QApplication([])
    
    window = MainWindow()
    window.show()
    
    app.exec()