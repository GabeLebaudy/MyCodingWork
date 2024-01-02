#This file will be used to store the widgets for the current set object. 

#Imports
import logging
import os
from decorators import log_start_and_stop

from PyQt6.QtWidgets import (
    QHBoxLayout, QVBoxLayout, QWidget,
    QLabel, QLineEdit, QSizePolicy,
    QPushButton, QSpacerItem, QTextEdit
)
from PyQt6.QtCore import Qt, QSize, pyqtSignal
from PyQt6.QtGui import QFont, QGuiApplication

#Logging
LOGGER = logging.getLogger('Main Logger')

#Node class
class Node:
    #Constructor
    def __init__(self, termWid, defWid, layout, removeBtn):
        self.termWid = termWid
        self.defWid = defWid
        self.pairLay = layout
        self.removeBtn = removeBtn
        
    #Getters
    def getTermWid(self):
        return self.termWid
    
    def getDefWid(self):
        return self.defWid
    
    def getLayout(self):
        return self.pairLay
    
    def getBtn(self):
        return self.removeBtn
    
    def getVals(self):
        return self.termWid.toPlainText(), self.defWid.toPlainText()
    
    #Setters
    def setTermVal(self, val):
        self.termWid.setText(val)
        
    def setDefVal(self, val):
        self.defWid.setText(val)
    
    #Delete widgets for the pair
    def delWidgets(self):
        self.termWid.deleteLater()
        self.defWid.deleteLater()
        self.removeBtn.deleteLater()
        self.pairLay.deleteLater()

    #Check if pair is empty 0:Completely empty, 1:At least one term is missing a definition pair 2: All good
    def checkEmpty(self):
        if not self.termWid.toPlainText() and not self.defWid.toPlainText():
            return 0
        if not self.termWid.toPlainText() or not self.defWid.toPlainText():
            return 1
        else: return 2

    
#Set Class
class Set:
    #Constructor
    def __init__(self):
        self.items = []
        
    #Add a pair to the set
    def addNode(self, term, definition, layout, removeBtn):
        newNode = Node(term, definition, layout, removeBtn)
        self.items.append(newNode)
        
    #Remove a node with a given index
    def removeNode(self, index):
        self.items[index].delWidgets()
        del self.items[index]

    #Get the length of the set
    def getLength(self):
        return len(self.items)
    
    #Get Term Value Pair in Config Form
    def getConfigData(self, index):
        td, dd = self.items[index].getVals()
        if not td or not dd:
            return False
        
        return '{}:{}'.format(td, dd)

    #Check if the set is empty
    def isEmpty(self):
        return len(self.items) == 0
    
    #Check if set is ready to be created - 0:Completely empty, 1:At least one term is missing a definition pair 2: All good
    @log_start_and_stop
    def isPairsEmpty(self):
        flag = False
        ce = 0
        for i in range(len(self.items)):
            code = self.items[i].checkEmpty()
            if code == 1:
                flag = True
            if code == 2:
                ce = 2

        if not flag:
            return ce
        else:
            return 1
        
    #Return Dictionary of Set Pairs
    @log_start_and_stop
    def getPairData(self):
        finalList = {}
        for i in range(self.getLength()):
            termText, defText = self.items[i].getVals()
            if termText:
                finalList[termText] = defText

        return finalList

class Sets:
    #Signals to Main File
    messageSignal = pyqtSignal(list)
    textInputSignal = pyqtSignal(list)
    
    #Constructor
    def __init__(self):
        #Intialize Config File Path
        self.config_path = os.path.join(os.path.dirname(__file__), 'sets_configs.txt')
        
        #Store Current Pair Widget Data
        self.current_pairs = []
        self.removePairSignals = []
        
        #Create the layout for create set
        self.createSetLayout()
        
    #Create the container for creating and editing a set
    def createSetLayout(self):
        #Get Scales
        screen_resolution = QGuiApplication.primaryScreen().availableGeometry()
        width, height = screen_resolution.width(), screen_resolution.height()
        self.widthScale = width / 1920
        self.heightScale = height / 1032
        
        #Set Object containing its data
        self.set = Set()
        self.removePairSignals = []

        self.createSetContainer = QWidget()
        containerLayout = QHBoxLayout()
        self.createSetLayout = QVBoxLayout()

        self.setTitleContainer = QWidget()
        self.setTitleLayout = QHBoxLayout()

        self.setModeLabel = QLabel('Create Set')

        setModeFont = QFont()
        setModeFont.setPointSize(32)
        setModeFont.setBold(True)

        self.setModeLabel.setFont(setModeFont)
        self.setTitleLayout.addWidget(self.setModeLabel)
        self.setTitleLayout.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        self.setTitleContainer.setLayout(self.setTitleLayout)

        #Change Set Name Layout
        self.changeSetNameContainer = QWidget()
        self.changeSetNameLayout = QHBoxLayout()

        changeNameLabel = QLabel('Set Name:')
        changeNameFont = QFont()
        changeNameFont.setPointSize(16)
        changeNameFont.setBold(True)
        changeNameLabel.setFont(changeNameFont)

        editSetNameFont = QFont()
        editSetNameFont.setPointSize(14)

        self.changeSetNameInput = QLineEdit()
        self.changeSetNameInput.setFont(editSetNameFont)
        self.changeSetNameInput.setFixedSize(int(300 * self.widthScale), int(30 * self.heightScale))
        self.changeSetNameInput.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Preferred)

        self.changeSetNameLayout.addWidget(changeNameLabel)
        self.changeSetNameLayout.addWidget(self.changeSetNameInput)
        self.changeSetNameLayout.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        self.changeSetNameContainer.setLayout(self.changeSetNameLayout)
        self.changeSetNameContainer.setHidden(True)

        #Terms / Definitions / Pairs
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
        
        self.createSetLayout.addWidget(self.setTitleContainer)
        self.createSetLayout.addWidget(self.changeSetNameContainer)
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

        self.finishSetContainer = QWidget()
        self.finishSetLayout = QHBoxLayout()

        self.finishSetButton = QPushButton("Create")
        self.finishSetButton.setFixedSize(int(125 * self.widthScale), int(50 * self.heightScale))
        self.finishSetButton.clicked.connect(self.finalizeSet)

        self.finishSetLayout.addWidget(self.finishSetButton)
        self.finishSetLayout.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        self.finishSetContainer.setLayout(self.finishSetLayout)

        #For editing a set
        self.finishEditContainer = QWidget()
        self.finishEditLayout = QHBoxLayout()

        self.cancelEditBtn = QPushButton('Cancel')
        self.finishEditingBtn = QPushButton('Finish')

        finishEditButtonSizes = QSize(int(125 * self.widthScale), int(50 * self.heightScale))
        self.cancelEditBtn.setFixedSize(finishEditButtonSizes)
        self.finishEditingBtn.setFixedSize(finishEditButtonSizes)

        self.cancelEditBtn.clicked.connect(self.cancelEdit)
        self.finishEditingBtn.clicked.connect(self.finishEdit)

        self.finishEditLayout.addWidget(self.cancelEditBtn)
        self.finishEditLayout.addStretch(2)
        self.finishEditLayout.addWidget(self.finishEditingBtn)
        self.finishEditLayout.addStretch(3)
        self.finishEditLayout.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.finishEditContainer.setLayout(self.finishEditLayout)
        self.finishEditContainer.setHidden(True)

        self.createSetLayout.addLayout(self.itemPairsLayout)
        self.createSetLayout.addSpacerItem(QSpacerItem(0, int(20 * self.heightScale), QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed))
        self.createSetLayout.addLayout(self.addPairLayout)
        self.createSetLayout.addWidget(self.finishSetContainer)
        self.createSetLayout.addWidget(self.finishEditContainer)
        self.createSetLayout.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignHCenter)

        containerLayout.addSpacerItem(QSpacerItem(0, 0, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum))
        containerLayout.addLayout(self.createSetLayout)
        containerLayout.addSpacerItem(QSpacerItem(0, 0, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum))
        self.createSetContainer.setLayout(containerLayout)
    
    #Get the container that contains the create set data
    def getSetContainer(self):
        return self.createSetContainer
    
    #Set Main Container Hidden
    def setHidden(self, status):
        self.createSetContainer.setHidden(status)
        
    #Add a pair to the create set menu
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
        newPair = Node(termInput, defInput, pairLayout, removeBtn)
        self.current_pairs.append(newPair)
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
            button = self.current_pairs[i].getBtn()
            buttonConnection = [button.clicked, removeFunc]
            buttonConnection[0].connect(buttonConnection[1])
            self.removePairSignals.append(buttonConnection)

    #Remove a pair from the set (Null is added so that index parameter won't get used by checked status of the button)
    def removeSetPair(self, index, null):
        self.current_pairs.pop(index)
        self.updatePairSignals()
    
    #Finish the creation of a new set
    @log_start_and_stop
    def finalizeSet(self, *args, **kwargs):
        emptyFlag = self.set.isPairsEmpty()

        if emptyFlag == 0:
            self.messageSignal.emit(['Error', 'At least one term is needed'])
            return
        elif emptyFlag == 1:
            self.messageSignal.emit(['Error', 'At least one pair is incomplete'])
            return
        
        #Prompt user for name for the set
        setName = self.textInputSignal.emit(['Dialog Title', 'Enter a name for this set:'])
        if not setName:
            return

        setVals = self.set.getPairData()
        with open(self.config_path, 'a') as file:
            title = '{}\n'.format(setName)
            file.write(title)
            for term in setVals:
                s = '{}:{}\n'.format(term, setVals[term])
                file.write(s)

        #Add title to dropdowns and side bar
        #TODO: Add SideBar Object, call methods from here
        #self.addSideBarSet(setName)
        #self.selectSetDD.addItem(setName)
        
        #Ping user that set was successfully created
        self.messageSignal.emit(['Success!', 'Your set {} was successfully created!'.format(setName)])

        #Reset the tab
        while not(self.set.isEmpty()):
            self.set.removeNode(0)
        
        for i in range(5):
            self.addSetPair()