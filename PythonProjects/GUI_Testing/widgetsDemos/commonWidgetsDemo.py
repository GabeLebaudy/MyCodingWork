from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QApplication,
    QCheckBox,
    QComboBox,
    QDateEdit,
    QDateTimeEdit,
    QDial,
    QDoubleSpinBox,
    QFontComboBox,
    QLabel,
    QLCDNumber,
    QLineEdit,
    QMainWindow,
    QProgressBar,
    QPushButton,
    QRadioButton,
    QSlider,
    QSpinBox,
    QTimeEdit,
    QVBoxLayout,
    QWidget,
)


# Subclass QMainWindow to customize your application's main window
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Widgets App")

        layout = QVBoxLayout() #Create Layout object
        widgets = [ #Create list with common widgets
            QCheckBox, #Binary check box
            QComboBox, #Drop down menu (CHECK)
            QDateEdit, #mm/dd/yyyy
            QDateTimeEdit, #mm/dd/yyyy hh:mm (AM/PM)
            QDial, #Large dial in middle
            QDoubleSpinBox, #Number spinner for float values
            QFontComboBox, #Choose font
            QLCDNumber, #LCD Display (Kinda ugly and niche)
            QLabel, #Label: Non-interactive
            QLineEdit, #Text input line
            QProgressBar, #Progress bar (Usually linked to something else)
            QPushButton, #Button
            QRadioButton, #Radio options means only one option can be selected
            QSlider, #Slider bar (Vertical in this case)
            QSpinBox, #Number spinner for int values
            QTimeEdit, #hh:mm (AM/PM)
        ]

        #Loop through widget list and add them to the layout object
        for w in widgets:
            layout.addWidget(w())

        widget = QWidget() #Create central widget object
        widget.setLayout(layout) #Set container's layout to be populated layout object

        # Set the central widget of the Window. Widget will expand
        # to take up all the space in the window by default.
        self.setCentralWidget(widget)

if __name__ == "__main__":
    app = QApplication([])
    window = MainWindow()
    window.show()

    app.exec()