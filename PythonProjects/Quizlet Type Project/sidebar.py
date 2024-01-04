#Used for storing the widgets, layouts and signals on the side bar

#Imports
from decorators import log_start_and_stop
from Sets import Sets

from PyQt6.QtWidgets import (
    QHBoxLayout, QVBoxLayout, QLabel,
    QPushButton
)
from PyQt6.QtCore import Qt, QObject, pyqtSignal
from PyQt6.QtGui import QFont, QGuiApplication
#Node Class
class Node:
    #Constructor
    def __init__(self, titleLabel, editBtn, delBtn, setLayout):
        self.titleLabel = titleLabel
        self.editBtn = editBtn
        self.delBtn = delBtn
        self.setLayout = setLayout
        
    #Getters
    def getTitle(self):
        return self.titleLabel
    
    def getEditBtn(self):
        return self.editBtn
    
    def getDelBtn(self):
        return self.delBtn
    
    def getSetLayout(self):
        return self.setLayout
    
    #Delete the node
    def deleteWidgets(self):
        self.titleLabel.deleteLater()
        self.editBtn.deleteLater()
        self.delBtn.deleteLater()
        self.setLayout.deleteLater()
        
#Side Bar class
class SideBar(QObject):
    
    yesOrNoSignal = pyqtSignal(list)

    #Constructor
    def __init__(self):
        #Initialize Parent Class
        super().__init__()

        #Storing and Modifying Widget Data
        self.items = []
        self.editSignals = []
        self.deleteSignals = []

        #Links to other files
        self.setData = Sets()

    #Create Layout
    @log_start_and_stop
    def generateSideBar(self):
        #Get Scales
        screen_resolution = QGuiApplication.primaryScreen().availableGeometry()
        width, height = screen_resolution.width(), screen_resolution.height()
        self.widthScale = width / 1920
        self.heightScale = height / 1032

        self.sideBarLayout = QVBoxLayout()
        self.sideBar = SideBar()
        
        sideBarLabel = QLabel("Your Sets")
        sideBarFont = QFont()
        sideBarFont.setPointSize(24)
        sideBarLabel.setFont(sideBarFont)
        
        self.sideBarLayout.addWidget(sideBarLabel)
        self.sideBarLayout.setAlignment(Qt.AlignmentFlag.AlignTop)
        
        self.sideBarLayout.addWidget(sideBarLabel)
        self.regenSideBar()

    #For access from main window
    def getLayout(self):
        return self.sideBarLayout
    
    #Add a pair to the set
    def addNode(self, title):
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
        
        newNode = Node(titleLabel, editBtn, deleteBtn, setLayout)
        self.items.append(newNode)

        self.updateSideBarSignals()

    #Update the signals of the edit button and the delete button for each set on the sidebar
    def updateSideBarSignals(self):
        self.sideBar.resetSignals()
        
        for i in range(len(self.items)):
            editFunction = lambda checked, x = i: self.promptEdit(x, checked)
            deleteFunction = lambda checked, x = i: self.promptDelete(x, checked)
            
            editButton = self.items[i].getEditBtn()
            deleteButton = self.items[i].getDelBtn()
            
            editButtonConnection = [editButton.clicked, editFunction]
            deleteButtonConnection = [deleteButton.clicked, deleteFunction]
            
            editButtonConnection[0].connect(editButtonConnection[1])
            deleteButtonConnection[0].connect(deleteButtonConnection[1])
            
            self.editSignals.append(editButtonConnection)
            self.deleteSignals.append(deleteButtonConnection)
        
    #Remove a node with a given index
    def removeNode(self, index):
        self.items[index].deleteWidgets()
        del self.items[index]

    #Refresh or Generate new Sidebar sets
    @log_start_and_stop
    def regenSideBar(self):
        #Remove old titles if necessary
        while len(self.items) > 0:
            self.removeNode(0)
        
        #Get all current titles and create nodes for them
        titles = self.setData.getAllSetTitles()
        for title in titles:
            self.addNode(title)
    
    #Reset the signals
    def resetSignals(self):
        for connection in self.editSignals:
            connection[0].disconnect()
            
        for connection in self.deleteSignals:
            connection[0].disconnect()
            
        self.editSignals, self.deleteSignals = [], []

    #Prompt an edit from the Sets File
    def promptEdit(self, index, null):
        code = self.setData.getCurrentData()
        if code != 0:
            confirmDialog = self.yesOrNoSignal(['Conflict', 'This action will clear all data in the Create Set tab.\n Are you sure you want to continue?', ['Yes', 'No']])
            if not confirmDialog:
                return
        
        self.setData.editSet(index)
        

    #Prompt a removal of a set from the sets file
    def promptDelete(self, index, null):
        setName = self.setData.getSetTitle(index)
        self.binaryAnswer = None
        
        self.yesOrNoSignal.emit(['Deletion Confirmation', 'Are you sure you want to delete the following set:\n{}?'.format(setName), ['Delete', 'Cancel']])
        if self.binaryAnswer:
            self.setData.deleteSet(setName)
            self.regenSideBar()
        
    #Change answer
    def setAnswer(self, answer):
        self.binaryAnswer = answer
