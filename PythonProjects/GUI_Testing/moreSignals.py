#Import modules
from PyQt6.QtWidgets import QApplication, QMainWindow, QLabel, QLineEdit, QVBoxLayout, QWidget

#window subclass
class MainWindow(QMainWindow):
    #Constructor method
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Another Examples of Signals")

        self.label = QLabel()

        self.input = QLineEdit()
        self.input.textChanged.connect(self.label.setText)

        layout = QVBoxLayout()
        layout.addWidget(self.input)
        layout.addWidget(self.label)

        container = QWidget()
        container.setLayout(layout)

        #Set Central widget of window
        self.setCentralWidget(container)

if __name__ == "__main__":
    app = QApplication([])

    window = MainWindow()
    window.show()

    app.exec()
