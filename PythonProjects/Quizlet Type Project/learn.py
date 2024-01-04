#This file will be used for the match game.

#Imports
import random
from decorators import log_start_and_stop
from Sets import Sets

from PyQt6.QtWidgets import ( 
    QHBoxLayout, QVBoxLayout, QWidget,
    QPushButton, QLineEdit, QSpacerItem,
    QLabel, QComboBox, QSizePolicy
)
from PyQt6.QtCore import QObject, Qt, pyqtSignal
from PyQt6.QtGui import QGuiApplication, QFont

#Question Class
class Question:
    #Constructor
    def __init__(self):
        self.question = None
        self.answer = None
        self.stage = 0 #0 for multiple choice, 1 for fill in the blank, 2 for direct answer

    #Getters
    def getQuestion(self):
        return self.question
    
    def getAnswer(self):
        return self.answer
    
    def getStage(self):
        return self.stage
    
    #Setters
    def setQuestion(self, q):
        self.question = q

    def setAnswer(self, a):
        self.answer = a

    def goNextStage(self):
        #TODO: depending on what parts of the learning process the user wants to use, this method will go to the next stage. If it completes the final stage, it should return a signal to remove the question from the stack
        self.stage += 1 

    #If the user chose the random gamemode, the question and answer should be randomized for each stage, not just the learn run
    def randomizeQandA(self):
        doSwitch = random.randint(0, 1)
        if doSwitch == 0:
            temp = self.question
            self.question = self.answer
            self.answer = temp
        
    
#Match Class
class Learn(QObject):
    #Signals
    messageSignal = pyqtSignal(list)

    #Constructor
    def __init__(self):
        #Call Parent Constructor method
        super().__init__()

        #Intialize Learn Variables
        self.questions = []
        self.gamemode = 0
        self.mixedFlag = 0

        #Access to Set data
        self.setData = Sets()

    #Generate The Match Container Layout
    def genMatchLayout(self):
        #Get Scales
        screen_resolution = QGuiApplication.primaryScreen().availableGeometry()
        width, height = screen_resolution.width(), screen_resolution.height()
        self.widthScale = width / 1920
        self.heightScale = height / 1032

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
        
        #Cancel Match Game Option
        self.cancelMatchContainer = QWidget()
        self.cancelMatchLayout = QHBoxLayout()
        
        self.cancelMatchBtn = QPushButton('Exit')
        self.cancelMatchBtn.clicked.connect(self.cancelMatch)
        
        self.cancelMatchLayout.addSpacerItem(QSpacerItem(int(300 * self.widthScale), 0, QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Minimum))
        self.cancelMatchLayout.addWidget(self.cancelMatchBtn)
        self.cancelMatchLayout.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.cancelMatchContainer.setLayout(self.cancelMatchLayout)
        self.cancelMatchContainer.setHidden(True)

        #Container for all match layouts
        self.matchMainLayout.addSpacerItem(QSpacerItem(0, 0, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum))
        self.matchMainLayout.addWidget(matchLabel)
        self.matchMainLayout.addSpacerItem(QSpacerItem(0, int(50 * self.heightScale), QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed))
        self.matchMainLayout.addWidget(self.startMatchContainer)
        self.matchMainLayout.addWidget(self.mainMatchQContainer)
        self.matchMainLayout.addWidget(self.answerCorrectContainer)
        self.matchMainLayout.addWidget(self.incorrectAnswerContainer)
        self.matchMainLayout.addWidget(self.matchCompletedContainer)
        self.matchMainLayout.addSpacerItem(QSpacerItem(0, int(40 * self.heightScale), QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed))
        self.matchMainLayout.addWidget(self.cancelMatchContainer)
        self.matchMainLayout.addSpacerItem(QSpacerItem(0, 0, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum))
        self.matchMainLayout.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignHCenter)
        self.matchContainer.setLayout(self.matchMainLayout)
        self.matchContainer.setHidden(True)

    #Get the layout container
    def getLearnContainer(self):
        return self.matchContainer
    
    #Show/Hide the Layout
    def setHidden(self, status):
        self.matchContainer.setHidden(True)

    #Populate the select set dropdown menu in the match tab
    def populateMatchDD(self):
        titles = self.setData.getAllSetTitles()

        for name in titles:
            self.selectSetDD.addItem(name)
    
    #Start the match game
    @log_start_and_stop
    def startMatch(self, *args, **kwargs):
        #Pull match parameters
        learn_set_name = self.selectSetDD.currentText()
        gamemode = self.matchOptionsDD.currentIndex()

        #Get Set Data using set name
        learn_set_data = self.setData.getSetContent(learn_set_name)

        #Ensure set is still available
        if not learn_set_data:
            self.messageSignal.emit(['Error', "The program couldn't find the set selected."])
            return 

        #Set the match gamemode from input
        self.setGamemode(gamemode)
        
        for item in learn_set_data:
            self.addQuestion(item)             
        
        #Shuffle the pairs
        self.shuffle()
        
        #Set match layout
        self.startMatchContainer.setHidden(True)
        self.mainMatchQContainer.setHidden(False)
        self.cancelMatchContainer.setHidden(False)
        
        #Initialize progress label info
        self.lenFullSet = len(self.questions)
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
        question = self.getQuestion()
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
        self.cancelMatchContainer.setHidden(True)
        self.matchCompletedContainer.setHidden(False)      

    #Replay set button   
    def replayMatchGame(self):
        self.matchCompletedContainer.setHidden(True)
        self.startMatch()

    #Reset match tab
    def resetMatchTab(self):
        self.matchCompletedContainer.setHidden(True)
        self.startMatchContainer.setHidden(False)

    #Cancel match mid-game
    def cancelMatch(self):
        self.match.resetGame()
        
        self.answerCorrectContainer.setHidden(True)
        self.incorrectAnswerContainer.setHidden(True)
        self.mainMatchQContainer.setHidden(True)
        self.cancelMatchContainer.setHidden(True)
        self.startMatchContainer.setHidden(False)  
    
    #Getter methods
    def getAllPairs(self):
        return self.questions
    
    def getPair(self, index):
        return self.questions[index]
    
    #Setter methods
    def setGamemode(self, mode):
        self.gamemode = mode
    
    #Check if set is empty
    def isEmpty(self):
        return len(self.questions) == 0
    
    #Check the length of the match set
    def getLength(self):
        return len(self.questions)
    
    #Construct the main storage of the match game
    def addQuestion(self, question):
        question_content = question.split(':')
        term, definition = question_content[0], question_content[1]
        q = Question()

        #Given definition, enter term
        if self.gamemode == 0:
            q.setQuestion(definition)
            q.setAnswer(term)
        #Given term, enter definition
        else:
            q.setQuestion(term)
            q.setAnswer(definition)

        #If the user selected random, randomize which is question and which is answer
        if self.gamemode == 2:
            q.randomizeQandA()
        
            
    #Randomize the set
    @log_start_and_stop
    def shuffle(self):
        temp = []
        while not self.isEmpty():
            randomInd = random.randint(0, len(self.questions) - 1)
            temp.append(self.questions[randomInd])
            del self.questions[randomInd]
        
        self.questions = temp

    #Get the next question from the set
    def getQuestion(self):
        #Given Definition, Match Term
        if self.gamemode == 0:
            return self.questions[0][1]
        
        #Given Term, Match Definition
        elif self.gamemode == 1:
            return self.questions[0][0]

        #Mixed
        else:
            termOrDef = random.randint(0, 1)
            self.mixedFlag = termOrDef
            return self.questions[0][termOrDef]
        
    #Return if user was right, and the answer string
    def isRight(self, userAnswer):
        if self.gamemode == 0:
            wasRight = self.questions[0][0].lower() == userAnswer.lower()
            return wasRight, self.questions[0][0]
        elif self.gamemode == 1:
            wasRight = self.questions[0][1].lower() == userAnswer.lower()
            return wasRight, self.questions[0][1]
        else:
            tupleIndex = 1 if self.mixedFlag == 0 else 0
            wasRight = self.questions[0][tupleIndex].lower() == userAnswer.lower()
            return wasRight, self.questions[0][tupleIndex]
        
    #Function for if user answered correctly
    @log_start_and_stop
    def answeredCorrect(self):
        self.questions.pop(0)

    #Function for if the user answered incorrectly
    @log_start_and_stop
    def reshuffleQuestion(self):
        item = self.questions.pop(0)
        if len(self.questions) >= 1:
            newIndex = random.randint(1, len(self.questions))
            self.questions.insert(newIndex, item)

    #Game is completed, reset the match obj
    def resetGame(self):
        self.questions = []
        self.gamemode = 0
        self.mixedFlag = 0
        