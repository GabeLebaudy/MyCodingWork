from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QRadioButton,
    QVBoxLayout, QLabel, QRadioButton,
    QWidget, QGroupBox
)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        layout = QVBoxLayout()

        radio_button = QRadioButton()
        
        temp = QVBoxLayout(radio_button)

        label = QLabel("This is a long text that needs word wrap word wrap word wrap word wrap word wrap word wrap", radio_button)
        label.setWordWrap(True)

        temp.addWidget(label)

        layout.addWidget(radio_button)

        widget = QWidget()
        widget.setLayout(layout)

        self.setCentralWidget(widget)

if __name__ == "__main__":
    app = QApplication([])

    window = MainWindow()
    window.show()

    app.exec()