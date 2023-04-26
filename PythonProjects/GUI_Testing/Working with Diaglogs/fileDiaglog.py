from PyQt6.QtWidgets import QApplication, QMainWindow, QFileDialog, QPushButton

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("File Dialog Example")
        self.setGeometry(100, 100, 400, 300)

        # Add a button to open the file dialog
        self.button = QPushButton("Open File", self)
        self.button.move(150, 100)
        self.button.clicked.connect(self.open_file_dialog)

    def open_file_dialog(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Open File", "", "CSV (*.csv)")
        # The first parameter is the parent widget, the second is the dialog title,
        # the third is the initial directory to open, and the fourth is the file filter.
        
        if file_path:
            print(f"Selected file: {file_path}")
            # Do something with the selected file

if __name__ == '__main__':
    app = QApplication([])
    
    window = MainWindow()
    window.show()
    
    app.exec()
