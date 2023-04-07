#Import modules
from PyQt6.QtWidgets import QApplication, QMainWindow, QLabel, QLineEdit, QVBoxLayout, QWidget

#window subclass
class MainWindow(QMainWindow):
    #Constructor method
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Another Examples of Signals")

        self.label = QLabel() #Adds label to Window Obj

        self.input = QLineEdit() #Adds textbox to Window Obj
        self.input.textChanged.connect(self.label.setText)#Sends signal when text input changes. Labels text is set to input's value

        layout = QVBoxLayout() #Create layout object
        layout.addWidget(self.input)#Add textbox to layout
        layout.addWidget(self.label)#Add label beneath textbox

        container = QWidget()#Container for layout object
        container.setLayout(layout)#Set layout of container to layout object

        #Set Central widget of window
        self.setCentralWidget(container)

if __name__ == "__main__":
    app = QApplication([])

    window = MainWindow()
    window.show()

    app.exec()
