from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QApplication, QLabel, QMainWindow, QTextEdit


#Window Subclass
class MainWindow(QMainWindow):
    #Constructor method
    def __init__(self):
        super().__init__()

        self.label = QLabel("Click Anywhere!")
        self.setCentralWidget(self.label)

    #Mouse events
    def mouseMoveEvent(self, e):
        self.label.setText("Mouse is moving! (and clicked lol)")

    def mousePressEvent(self, e):
        if e.button() == Qt.MouseButton.LeftButton:
            self.label.setText("Left Click!")
        elif e.button() == Qt.MouseButton.MiddleButton:
            self.label.setText("Wow you're a weirdo")
        elif e.button() == Qt.MouseButton.RightButton:
            self.label.setText("Right Click")
    
    def mouseReleaseEvent(self, e):
        if e.button() == Qt.MouseButton.LeftButton:
            self.label.setText("Left Click Released!")
        elif e.button() == Qt.MouseButton.MiddleButton:
            self.label.setText("Thank God you're done man wtf was that?")
        elif e.button() == Qt.MouseButton.RightButton:
            self.label.setText("Right Click Released!")

    def mouseDoubleClickEvent(self, e):
        if e.button() == Qt.MouseButton.LeftButton:
            self.label.setText("Double Left Click!")
        elif e.button() == Qt.MouseButton.MiddleButton:
            self.label.setText("Don't ever talk to me again.")
        elif e.button() == Qt.MouseButton.RightButton:
            self.label.setText("Double Right Click")
        

#Main Script
if __name__ == "__main__":
    app = QApplication([])

    window = MainWindow()
    window.show()

    app.exec()