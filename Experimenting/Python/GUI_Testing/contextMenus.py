#Import modules
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QAction
from PyQt6.QtWidgets import QApplication, QLabel, QMainWindow, QMenu

#Main Window Subclass
class MainWindow(QMainWindow):
    #Constructor method
    def __init__(self):
        super().__init__()

        '''
        #Alternate way of creating context menu
        self.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.customContextMenuRequested.connect(self.alternateContextMenu)
        '''
    #Context menu event
    def contextMenuEvent(self, e):
        context = QMenu(self)
        context.addAction(QAction("Copy", self))
        context.addAction(QAction("Paste", self))
        context.addAction(QAction("Delete", self))
        context.exec(e.globalPos())
    
    def alternateContextMenu(self, pos):
        context = QMenu(self)
        context.addAction(QAction("Copy", self))
        context.addAction(QAction("Paste", self))
        context.addAction(QAction("Delete", self))
        context.exec(self.mapToGlobal(pos))

#Main Script
if __name__ == "__main__":
    app = QApplication([])

    window = MainWindow()
    window.show()

    app.exec()