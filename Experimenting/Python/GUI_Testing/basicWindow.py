from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton
from PyQt6.QtCore import QSize, Qt 

#Use a class to add widgets to a window
class MainWindow(QMainWindow):
    #Constructor method
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Testing PyQT6!") #Sets Window Title (Obv)
        button = QPushButton("Export") #Create new button with argument being the displayed text
        
        self.setCentralWidget(button)#Places widget: Defaults to fit window size
        
        #self.setFixedSize(QSize(400, 300)) #Creates window with width and height and doesn't allow resizing
        
        #.setMinimumSize() and setMaximumSize() set the minimum and maximum size of the widget (shocker)

if __name__ == "__main__":
    #Only one QApplication per script.
    app = QApplication([])

    #Create Qt Widget which will be the window
    window = MainWindow()
    window.show()

    #Start event loop
    app.exec()
