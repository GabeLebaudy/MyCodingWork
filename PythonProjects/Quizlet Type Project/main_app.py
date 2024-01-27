#This file will be the main app for the Quizlet match game 

#Imports
import logging
import os
from PyQt6.QtWidgets import (
    QMainWindow, QApplication, QLineEdit,
    QLabel, QPushButton, QDialog,
    QHBoxLayout, QVBoxLayout, QSizePolicy, 
    QWidget, QSpacerItem, QDialogButtonBox
)
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QGuiApplication, QFont
from Sets import Sets
from sidebar import SideBar
from learn import Learn
from quiz import Quiz
from flashcards import FlashCards
from decorators import log_start_and_stop


#Logging Setup
LOGGER = logging.getLogger('Main Logger')
#Filepath to set information file
SETS_CONFIG_PATH = os.path.join(os.path.dirname(__file__), 'sets_configs.txt')

#Main Window Class
class MainWindow(QMainWindow):
    #Create title bar
    @log_start_and_stop
    def createTitleBar(self):
        self.titleBarLayout = QHBoxLayout()
        
        self.createSetButton = QPushButton("Create Set")
        self.flashCardsBtn = QPushButton("Flash Cards")
        self.playLearnButton = QPushButton("Learn")
        self.playQuizButton = QPushButton("Quiz")

        buttonSizes = QSize(int(150 * self.widthScale), int(75 * self.heightScale))
        
        self.createSetButton.setFixedSize(buttonSizes)
        self.createSetButton.clicked.connect(self.navCreateSet)
        
        self.flashCardsBtn.setFixedSize(buttonSizes)
        self.flashCardsBtn.clicked.connect(self.navFlashCards)

        self.playLearnButton.setFixedSize(buttonSizes)
        self.playLearnButton.clicked.connect(self.navLearn)

        self.playQuizButton.setFixedSize(buttonSizes)
        self.playQuizButton.clicked.connect(self.navQuiz)
        
        self.titleBarLayout.addWidget(self.createSetButton)
        self.titleBarLayout.addWidget(self.flashCardsBtn)
        self.titleBarLayout.addWidget(self.playLearnButton)
        self.titleBarLayout.addWidget(self.playQuizButton)
        self.titleBarLayout.setAlignment(Qt.AlignmentFlag.AlignLeft)

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
        self.SideBar = SideBar()
        self.SideBar.generateSideBar()
        self.side_bar_container = self.SideBar.getLayout()

        self.Sets = Sets()
        self.create_set_container = self.Sets.getSetContainer()

        self.Flashcards = FlashCards()
        self.flashContainer = self.Flashcards.getContainer()

        self.LearnObj = Learn()
        self.LearnObj.genLearnLayout()
        self.learn_container = self.LearnObj.getLearnContainer()

        self.QuizObj = Quiz()
        self.quiz_container = self.QuizObj.genMainContainer()

        self.completeLayout = QHBoxLayout()
        self.mainAreaLayout = QVBoxLayout()
        
        self.mainAreaLayout.addLayout(self.titleBarLayout)
        self.mainAreaLayout.addSpacerItem(QSpacerItem(0, int(30 * self.heightScale), QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed))
        self.mainAreaLayout.addWidget(self.create_set_container)
        self.mainAreaLayout.addWidget(self.learn_container)
        self.mainAreaLayout.addWidget(self.flashContainer)
        self.mainAreaLayout.addWidget(self.quiz_container)
        self.mainAreaLayout.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        
        self.completeLayout.addSpacerItem(QSpacerItem(int(25 * self.widthScale), 0, QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Minimum))
        self.completeLayout.addLayout(self.side_bar_container)
        self.completeLayout.addSpacerItem(QSpacerItem(int(50 * self.widthScale), 0, QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Minimum))
        self.completeLayout.addLayout(self.mainAreaLayout)
        self.completeLayout.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft)
        
        centralWidget = QWidget()
        centralWidget.setLayout(self.completeLayout)
        self.setCentralWidget(centralWidget)
        
        #Signals
        self.Sets.messageSignal.connect(self.handleMessageSignal)
        self.Sets.textInputSignal.connect(self.handleSetTextInputSignal)
        self.Sets.newSetSignal.connect(self.handleNewSet)
        self.Sets.binaryAnswerSignal.connect(self.handleSetBinarySignal)
        self.Sets.editDoneSignal.connect(self.handleEditCompleteSignal)
        self.Sets.setsChangedSignal.connect(self.handleSetListUpdate)
        
        self.SideBar.deleteSetSignal.connect(self.handleDeleteSetSignal)
        self.SideBar.editSetDialogSignal.connect(self.handleEditSetDialogSignal)
        self.SideBar.getDataSignal.connect(self.handleGetSetData)
        self.SideBar.editSetSignal.connect(self.handleEditSetSignal)
        self.SideBar.navSignal.connect(self.navCreateSet)
        self.SideBar.setsChangedSignal.connect(self.handleSetListUpdate)

        self.LearnObj.messageSignal.connect(self.handleMessageSignal)

        self.QuizObj.message_signal.connect(self.handleMessageSignal)
        
        
    #----------------------
    # Navigation Methods
    #----------------------
    
    #Switch to create set tab
    def navCreateSet(self):
        self.LearnObj.setHidden(True)
        self.Flashcards.setHidden(True)
        self.QuizObj.setHidden(True)
        self.Sets.setHidden(False)

    #Switch to match tab
    def navLearn(self):
        self.Sets.setHidden(True)
        self.Flashcards.setHidden(True)
        self.QuizObj.setHidden(True)
        self.LearnObj.setHidden(False)
        
    #Switch to FlashCards Tab
    def navFlashCards(self):
        self.Sets.setHidden(True)
        self.LearnObj.setHidden(True)
        self.QuizObj.setHidden(True)
        self.Flashcards.setHidden(False)

    #Switch to Quiz Tab
    def navQuiz(self):
        self.Sets.setHidden(True)
        self.LearnObj.setHidden(True)
        self.Flashcards.setHidden(True)
        self.QuizObj.setHidden(False)
        
    
    #----------------------------------
    # Signal Handling Methods
    #----------------------------------
        
    #Set was deleted, update the side bar
    def handleSideBarUpdate(self):
        self.SideBar.regenSideBar()
    
    #Signal sent from sidebar file, used to delete a set from the app
    def handleDeleteSetSignal(self, contents):
        answer = self.yesOrNoDialog(contents[0], contents[1], contents[2])
        self.SideBar.setAnswer(answer)
    
    #Signal send from sidebar file, used to confirm with user that all current data will be lost
    def handleEditSetDialogSignal(self, contents):
        answer = self.yesOrNoDialog(contents[0], contents[1], contents[2])
        self.SideBar.confirmEditDialog = answer
    
    #Signal sent from sidebar file, used to prompt an edit screen.
    def handleEditSetSignal(self, title):
        self.Sets.editSet(title)

    #Edit Done
    def handleEditCompleteSignal(self):
        self.SideBar.enableDelete(True)
        self.SideBar.regenSideBar()

    #Set list is updated
    def handleSetListUpdate(self):
        self.Flashcards.populateSetDD()
        self.LearnObj.populateSetDD()
        self.QuizObj.populateSetDD()

    #New Set Created, route signal to sidebar file
    def handleNewSet(self, title):
        self.SideBar.addNode(title)
    
    #Getting the current data from the Sets object
    def handleGetSetData(self):
        currentData = self.Sets.getCurrentData()
        self.SideBar.setCurrentData(currentData)
        
    #For receiving a message signal from any File
    def handleMessageSignal(self, contents):
        self.openMessageDialog(contents[0], contents[1])
    
    #For receiving a prompt for a text input from another file
    def handleSetTextInputSignal(self, contents):
        input = self.textInputDialog(contents[0], contents[1])
        self.Sets.changeSetName(input)
        
    #For giving a binary answer to the set file
    def handleSetBinarySignal(self, contents):
        ans = self.yesOrNoDialog(contents[0], contents[1], contents[2])
        self.Sets.binaryAnswer = ans
    
    #----------------------
    # Dialog Methods
    #----------------------
    
    #Standard message dialog
    @log_start_and_stop
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
    @log_start_and_stop
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
    
    #Prompt user for a yes or no answer
    def yesOrNoDialog(self, title, prompt, buttonText):
        confirmDialog = QDialog(self)
        confirmDialog.setWindowTitle(title)
        
        dialogLayout = QVBoxLayout()
        removeDialogLayout = QHBoxLayout()

        okBtn = QPushButton(buttonText[0])
        cancelBtn = QPushButton(buttonText[1])

        removeButtonBox = QDialogButtonBox()
        removeButtonBox.addButton(okBtn, QDialogButtonBox.ButtonRole.AcceptRole)
        removeButtonBox.addButton(cancelBtn, QDialogButtonBox.ButtonRole.RejectRole)
        
        removeButtonBox.accepted.connect(confirmDialog.accept)
        removeButtonBox.rejected.connect(confirmDialog.reject)
        
        dialogMessage = QLabel(prompt)
        messageFont = QFont()
        messageFont.setPointSize(14)
        dialogMessage.setFont(messageFont)
        dialogMessage.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignHCenter)
        removeDialogLayout.addWidget(dialogMessage)
        
        hbox = QHBoxLayout()
        hbox.addWidget(okBtn)
        hbox.addStretch(1)
        hbox.addWidget(cancelBtn)
        
        dialogLayout.addLayout(removeDialogLayout)
        dialogLayout.addLayout(hbox)
        confirmDialog.setLayout(dialogLayout)
        
        if confirmDialog.exec() == QDialog.DialogCode.Accepted:
            return True
        else:
            return False
    
#Main Method
if __name__ == "__main__":
    app = QApplication([])
    
    window = MainWindow()
    window.show()
    
    app.exec()