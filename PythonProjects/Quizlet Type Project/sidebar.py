#Used for storing the widgets, layouts and signals on the side bar

#Imports
from decorators import log_start_and_stop
from Sets import Sets
 
from PyQt6.QtWidgets import (
    QHBoxLayout, QVBoxLayout, QLabel,
    QPushButton, QWidget, QScrollArea,
    QSizePolicy, QSpacerItem
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
    
    #Change whether a set is able to be deleted (Disabled when editing a set)
    def setDeleteButtonStatus(self, s):
        self.delBtn.setEnabled(s)

    #Hide all the widgets(Implemented for that unfixable error)
    def setHidden(self):
        self.titleLabel.setHidden(True)
        self.editBtn.setHidden(True)
        self.delBtn.setHidden(True)

    #Delete the node
    def deleteWidgets(self):
        self.titleLabel.deleteLater()
        self.editBtn.deleteLater()
        self.delBtn.deleteLater()
        self.setLayout.deleteLater()
        
#Side Bar class
class SideBar(QObject):
    
    deleteSetSignal = pyqtSignal(list)
    editSetDialogSignal = pyqtSignal(list)
    editSetSignal = pyqtSignal(str)
    getDataSignal = pyqtSignal()
    navSignal = pyqtSignal()
    setsChangedSignal = pyqtSignal()

    
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

        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)

        self.scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOn)
        self.scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOn)
        self.scroll_area.setSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        sideBarWidget = QWidget()
        self.node_layout = QVBoxLayout()
        self.node_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        sideBarWidget.setLayout(self.node_layout)
        self.scroll_area.setWidget(sideBarWidget)

        self.sideBarLayout.addWidget(self.scroll_area)

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

        titleLabel.setFixedWidth(int(125 * self.widthScale))
        titleLabel.setWordWrap(True)
        titleLabel.setFixedHeight(titleLabel.sizeHint().height())
  
        setLayout.addWidget(titleLabel)
        setLayout.addWidget(editBtn)
        setLayout.addWidget(deleteBtn)
        setLayout.setAlignment(Qt.AlignmentFlag.AlignLeft)
        
        self.node_layout.addLayout(setLayout)
        
        newNode = Node(titleLabel, editBtn, deleteBtn, setLayout)
        self.items.append(newNode)
        
        #Update Side bar Length
        self.scroll_area.setMinimumWidth(self.scroll_area.sizeHint().width())

        self.updateSideBarSignals()

    #Update the signals of the edit button and the delete button for each set on the sidebar
    def updateSideBarSignals(self):    
        self.resetSignals()
        
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

        #Hide the first one to prevent errors
        if self.items:
            self.items[0].setHidden()
    
    #Reset the signals
    def resetSignals(self):        
        for edit_connection in self.editSignals:
            edit_connection[0].disconnect()
        
        for delete_connection in self.deleteSignals:
            delete_connection[0].disconnect()

        self.editSignals, self.deleteSignals = [], []

    #Prompt an edit from the Sets File
    def promptEdit(self, index, null):
        self.currentSetData = None
        self.getDataSignal.emit()
        
        if self.currentSetData != 0:
            self.confirmEditDialog = None
            self.editSetDialogSignal.emit(['Conflict', 'This action will clear all data in the Create Set tab.\n Are you sure you want to continue?', ['Yes', 'No']])
            
            if not self.confirmEditDialog:
                return

        #Disable ability to delete a set while currently editing
        self.enableDelete(False)

        setTitle = self.setData.getSetTitle(index)
        self.editSetSignal.emit(setTitle)

        #Ensure create tab is selected
        self.navSignal.emit()
        
    #Get the current data from the sets object
    def setCurrentData(self, data):
        self.currentSetData = data
    
    #Prompt a removal of a set from the sets file
    def promptDelete(self, index, null):
        setName = self.setData.getSetTitle(index)
        self.binaryAnswer = None
        
        self.deleteSetSignal.emit(['Deletion Confirmation', 'Are you sure you want to delete the following set:\n{}?'.format(setName), ['Delete', 'Cancel']])
        if self.binaryAnswer:
            self.setData.deleteSet(setName)
            self.regenSideBar()

            #Update set dropdowns in game menus
            self.setsChangedSignal.emit()
        
    #Change answer
    def setAnswer(self, answer):
        self.binaryAnswer = answer

    #Change ability to delete a set
    def enableDelete(self, status):
        for node in self.items:
            node.setDeleteButtonStatus(status)
