#This file will be used to store the widgets for the current set object. 

#Imports
import logging
import os
import re
from decorators import log_start_and_stop

from PyQt6.QtWidgets import (
    QHBoxLayout, QVBoxLayout, QWidget,
    QLabel, QLineEdit, QSizePolicy,
    QPushButton, QSpacerItem, QTextEdit,
    QScrollArea
)
from PyQt6.QtCore import Qt, QSize, pyqtSignal, QObject
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
    
class Sets(QObject):
    #Signals to Main File
    messageSignal = pyqtSignal(list)
    textInputSignal = pyqtSignal(list)
    binaryAnswerSignal = pyqtSignal(list)
    newSetSignal = pyqtSignal(str)
    editDoneSignal = pyqtSignal()
    setsChangedSignal = pyqtSignal()
    
    #Constructor
    def __init__(self):
        #Initiate Parent Class
        super().__init__()

        #Intialize Config File Path
        self.config_path = os.path.join(os.path.dirname(__file__), 'sets_configs.txt')
        
        #Store Current Pair Widget Data
        self.current_pairs = []
        self.removePairSignals = []
        self.termSignals = []
        self.defSignals = []

        #Generate layout as it will be difficult to interact from elsewhere without it
        self.createSetsLayout()
    
    #----------------------------------------
    # General Sets Info
    #----------------------------------------
    
    #Create the container for creating and editing a set
    def createSetsLayout(self):
        #Get Scales
        screen_resolution = QGuiApplication.primaryScreen().availableGeometry()
        width, height = screen_resolution.width(), screen_resolution.height()
        self.widthScale = width / 1920
        self.heightScale = height / 1032

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
        
        sets_scroll_area = QScrollArea()
        sets_scroll_area.setWidgetResizable(True)

        sets_scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOn)
        sets_scroll_area.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Expanding)

        sets_scroll_area.setFixedWidth(int(1250 * self.widthScale))

        scroll_widget = QWidget()
        sets_scroll_layout = QVBoxLayout()

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

        sets_scroll_layout.addLayout(self.itemPairsLayout)
        self.createSetLayout.addSpacerItem(QSpacerItem(0, int(20 * self.heightScale), QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed))
        sets_scroll_layout.addLayout(self.addPairLayout)

        scroll_widget.setLayout(sets_scroll_layout)
        sets_scroll_area.setWidget(scroll_widget)

        self.createSetLayout.addWidget(sets_scroll_area)
        self.createSetLayout.addWidget(self.finishSetContainer)
        self.createSetLayout.addWidget(self.finishEditContainer)
        self.createSetLayout.addSpacing(int(50 * self.heightScale))
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
    
    #Get a title from the config file given an index
    def getSetTitle(self, index):
        #Initialize flag and counter
        found = False
        counter = 0

        #Open config file
        with open(self.config_path, 'r') as file:
            while not found:
                line = file.readline().rstrip()
                if ':' not in line:
                    if counter == index:
                        return line
                    else:
                        counter += 1
                
                if not line:
                    return False
    
    #Get the set content in list form given the title
    def getSetContent(self, set_title):
        #Start reading file
        with open(self.config_path, 'r') as f:
            found = False
            startData = False
            content = []
            while not found:
                line = f.readline().rstrip()
                if not line:
                    break
                
                if line == set_title:
                    startData = True
                    continue

                if startData:
                    if ':' not in line:
                        found = True
                    else:
                        content.append(line)

        return content
    
    #There are a few times when all titles are needed, so this function grabs all of them
    def getAllSetTitles(self):
        #Read all data from file
        with open(self.config_path, 'r') as f:
            complete_data = f.readlines()
        
        titles = []
        for line in complete_data:
            if ':' not in line:
                titles.append(line.rstrip())
        
        return titles

    #Get the current data in the set menu. If completely empty, it returns 0, if at least one pair is missing it's opposite, returns 1. Otherwise it returns the data
    def getCurrentData(self):
        complete_data = []
        terms = []
        defs = []
        for node in self.current_pairs:
            term, definition = node.getVals()
            #Make sure pairs are not empty or missing values
            if not term and not definition:
                continue
            if not term or not definition:
                return 1
            
            #Make sure there are no duplicates
            if term in terms:
                return 2
            
            if definition in defs:
                return 3
            
            if re.search(r"[:\n]+", term):
                return 4
            
            if re.search(r"[:\n]+", definition):
                return 5
            
            terms.append(term)
            defs.append(definition)

            dataStr = term + ':' + definition
            complete_data.append(dataStr)
        
        if len(complete_data) > 0:
            return complete_data
        else:
            return 0
        
    #-------------------------------------------
    # Functions for creating a new set
    #-------------------------------------------

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

        termInput.setTabChangesFocus(True)
        defInput.setTabChangesFocus(True)

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
        for i in range(len(self.current_pairs)):
            removeFunc = lambda checked, x=i: self.removeSetPair(x, checked)
            button = self.current_pairs[i].getBtn()
            buttonConnection = [button.clicked, removeFunc]
            buttonConnection[0].connect(buttonConnection[1])
            self.removePairSignals.append(buttonConnection)

    #Remove a pair from the set (Null is added so that index parameter won't get used by checked status of the button)
    def removeSetPair(self, index, null):
        self.current_pairs[index].delWidgets()
        del self.current_pairs[index]
        self.updatePairSignals()
    
    #Finish the creation of a new set
    @log_start_and_stop
    def finalizeSet(self, *args, **kwargs):
        self.setName = None
        finalSetData = self.getCurrentData()
        
        #Check for any errors
        isErrors = self.checkErrors(finalSetData)
        if not isErrors:
            return
        
        #Prompt user for name for the set
        all_titles = self.getAllSetTitles()
        while not self.setName:
            self.textInputSignal.emit(['Dialog Title', 'Enter a name for this set:'])
            if re.search(r"[:\n]+", self.setName):
                self.messageSignal.emit(['Error', 'Set name cannot contain ":" character or a line break'])
                self.setName = None
            
            if self.setName in all_titles:
                self.messageSignal.emit(['Error', 'Set name already exists.'])
                self.setName = None

        with open(self.config_path, 'a') as file:
            title = '{}\n'.format(self.setName)
            file.write(title)
            for pair in finalSetData:
                s = '{}\n'.format(pair)
                file.write(s)

        #Add title to dropdowns and side bar
        self.newSetSignal.emit(self.setName)
        
        #Ping user that set was successfully created
        self.messageSignal.emit(['Success!', 'Your set {} was successfully created!'.format(self.setName)])

        #Reset the tab
        while len(self.current_pairs) > 0:
            self.removeSetPair(0, None)
        
        for i in range(5):
            self.addSetPair()

        #Update dropdowns in other sections
        self.setsChangedSignal.emit()

    #For getting user input from a dialog message. Controlled from main window
    def changeSetName(self, name):
        self.setName = name
        
    #Check for errors in current pairs
    def checkErrors(self, data):
        if data == 0: #Empty set
            self.messageSignal.emit(['Error', 'At least one pair is needed'])
            return False
        
        elif data == 1: #One pair is missing a term or definition
            self.messageSignal.emit(['Error', 'At least one pair is incomplete'])
            return False
        
        elif data == 2: #Duplicate Terms
            self.messageSignal.emit(['Error', 'One of the pairs contains a duplicate term.'])
            return False
        
        elif data == 3: #Duplicate definitions
            self.messageSignal.emit(['Error', 'One of the pairs contains a duplicate definition'])
            return False
        
        elif data == 4: #Term contains illegal character
            self.messageSignal.emit(['Error', r'At least one term contains a ":" or line break which is not allowed.'])
            return False
        
        elif data == 5: #Definition Contains Illegal Character
            self.messageSignal.emit(['Error', r'At least one definition contains a ":" or line break which is not allowed.'])
            return False
        
        else:
            return True
        
    #--------------------------------------------
    # Functions for editing or deleting a set
    #--------------------------------------------
            
    #Edit a set
    def editSet(self, name): 
        #Clear Previous Set
        while len(self.current_pairs) > 0:
            self.removeSetPair(0, None)
            
        #Pull set information
        self.currentSetName = name
        with open(self.config_path, 'r') as file:
            data = file.readlines()
            
        startInd, stopInd = self.findSetIndexes(data, name)
        if stopInd == 0:
            setData = data[startInd + 1:]
        else:
            setData = data[startInd + 1:stopInd]
        
        for pair in setData:
            #Create new widgets
            self.addSetPair()
            
            #Fill in Pairs with data
            pairItems = pair.rstrip().split(':')
            self.current_pairs[-1].setTermVal(pairItems[0])
            self.current_pairs[-1].setDefVal(pairItems[1])
        
        #Hide the create button layout, and 
        self.finishSetContainer.setHidden(True)
        self.changeSetNameContainer.setHidden(False)
        self.finishEditContainer.setHidden(False)
        self.setModeLabel.setText('Edit Set')
        self.changeSetNameInput.setText(name)

    #Cancle Current Edits 
    def cancelEdit(self):
        if self.wasEditChanges():
            self.binaryAnswer = None
            self.binaryAnswerSignal.emit(['Confirm', 'Are you sure you want to cancel editing?\nAll changes made will be lost.', ['Confirm', 'Continue Editing']])
            
            if self.binaryAnswer:
                self.revertToDefaultPageSet()
                self.editDoneSignal.emit()
                return
        else:
            self.revertToDefaultPageSet()
            self.editDoneSignal.emit()
        
    #Finish Edit
    def finishEdit(self):
        #Check if the user made any changes
        if not self.wasEditChanges():
            self.revertToDefaultPageSet()
            self.editDoneSignal.emit()
            return

        #Check if any data is incomplete
        newData = self.getCurrentData()
        
        #Check for errors
        isErrors = self.checkErrors(newData)
        if not isErrors:
            return
                
        #Pull File Data
        with open(self.config_path, 'r') as file:
            data = file.readlines()

        #Get Indexes of Current Set
        st, so = self.findSetIndexes(data, self.currentSetName)

        #Pull data from current inputs
        newSetName = self.changeSetNameInput.text()
        if re.search(r"[:\n]+", newSetName):
            self.messageSignal.emit(['Error', 'Set name cannot contain ":" or a line break.'])
            return

        #Create segment to overwrite with
        newSegment = [newSetName + '\n']
        for i in range(len(newData)):
            newSegment.append(newData[i] + '\n')

        if so != 0:
            data = data[:st] + newSegment + data[so:]
        else:
            data = data = data[:st] + newSegment

        #Write Complete Data back to set
        with open(self.config_path, 'w') as file:
            for line in data:
                file.write(line)
        
        #Confirm To User that set was completed
        self.messageSignal.emit(['Sucess!', 'Your new changes are successful'])
        self.revertToDefaultPageSet()
        self.editDoneSignal.emit()

    #Checks if user had made any changes a set
    @log_start_and_stop
    def wasEditChanges(self):
        #Pull data from the set
        setName = self.changeSetNameInput.text()

        #Compare Set Names
        if setName != self.currentSetName:
            LOGGER.info('Name')
            return True
        
        #Get Current Edited Data
        for i in range(len(self.current_pairs)):
            data = self.getCurrentData()
            try:
                data = int(data)
                return True
            except:
                pass

        #Get File Data
        with open(self.config_path, 'r') as file:
            fileData = file.readlines()

        #Find set indexes
        startI, stopI = self.findSetIndexes(fileData, self.currentSetName)

        if stopI != 0:
            setSegment = fileData[startI: stopI]
        else:
            setSegment = fileData[startI:]
        
        #If lengths are different, return true
        if len(data) + 1 != len(setSegment):
            LOGGER.info('{}, {}'.format(len(data), len(setSegment)))
            return True
        
        #Compare Terms
        flag = False
        for i in range(len(data)):
            if not setSegment[i + 1].rstrip() == data[i]:
                LOGGER.info('Flag')
                LOGGER.info("{}:{}".format(fileData[i + 1].rstrip(), data[i]))
                flag = True
        
        return flag
    
    #Revert back to create set page
    def revertToDefaultPageSet(self):
        #Delete Previous Pairs
        while len(self.current_pairs) > 0:
            self.removeSetPair(0, None)

        #Add 5 Empty Pairs
        for i in range(5):
            self.addSetPair()

        #Layouts
        self.changeSetNameContainer.setHidden(True)
        self.finishEditContainer.setHidden(True)
        self.finishSetContainer.setHidden(False)
        self.setModeLabel.setText('Create Set')

    #Delete a set from the list
    @log_start_and_stop
    def deleteSet(self, setName):
        #User confirmed the deletion of the set
        with open(self.config_path, 'r') as file:
            setsData = file.readlines()

        #Get indexes of set in the config file
        startIndex, stopIndex = self.findSetIndexes(setsData, setName)

        #Use indexes to exclude set from complete data
        if startIndex > 0:
            firstSection = setsData[:startIndex]
        else:
            firstSection = []

        if not(stopIndex == 0):
            secondSection = setsData[stopIndex:]
        else:
            secondSection = []

        #Overwrite file with new comlete data
        removedSetData = firstSection + secondSection
        with open(self.config_path, 'w') as file:
            for line in removedSetData:
                file.write(line)

    
    #Get the indexes of the set in the config file
    def findSetIndexes(self, setsData, setName):
        startIndex, stopIndex = 0, 0
        for i in range(len(setsData)):
            if setsData[i].rstrip() == setName:
                startIndex = i
                break
        
        for i in range(startIndex + 1, len(setsData)):
            if not(':' in setsData[i].rstrip()):
                stopIndex = i
                break   
            
        return startIndex, stopIndex     