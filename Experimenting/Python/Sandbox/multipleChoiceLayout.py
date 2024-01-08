#This will be a temporary file for creating the multiple choice layout for the learn game in the quizlet project

#Imports
from PyQt6.QtWidgets import (
    QHBoxLayout, QVBoxLayout, QMainWindow,
    QApplication, QLabel, QRadioButton,
    QPushButton, QSpacerItem, QWidget
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont

#Main Window Class
class MainWindow(QMainWindow):
    #Constructor
    def __init__(self):
        super().__init__()

        self.mult_choice_main_container = QWidget()
        mult_choice_main_layout = QVBoxLayout()

        mult_choice_question_layout = QHBoxLayout()

        self.mult_choice_question_label = QLabel('Sample Question')
        mult_choice_question_font = QFont()
        mult_choice_question_font.setPointSize(14)
        mult_choice_question_font.setBold(True)
        self.mult_choice_question_label.setFont(mult_choice_question_font)

        mult_choice_question_layout.addWidget(self.mult_choice_question_label)
        mult_choice_question_layout.setAlignment(Qt.AlignmentFlag.AlignHCenter)

        mult_choice_answers_layout = QVBoxLayout()
        
        self.mult_choice_answers = []
        for i in range(4):
            new_button = QRadioButton("Option {}".format(i + 1))
            self.mult_choice_answers.append(new_button)
            mult_choice_answers_layout.addWidget(new_button)

        mult_choice_answers_layout.setAlignment(Qt.AlignmentFlag.AlignLeft)

        mult_choice_check_layout = QHBoxLayout()
        
        mult_choice_check_button = QPushButton("Check Answer")

        mult_choice_check_layout.addWidget(mult_choice_check_button)
        mult_choice_check_layout.setAlignment(Qt.AlignmentFlag.AlignRight)

        mult_choice_main_layout.addLayout(mult_choice_question_layout)
        mult_choice_main_layout.addLayout(mult_choice_answers_layout)
        mult_choice_main_layout.addLayout(mult_choice_check_layout)
        self.mult_choice_main_container.setLayout(mult_choice_main_layout)

        self.setCentralWidget(self.mult_choice_main_container)

#Main Method
if __name__ == "__main__":
    app = QApplication([])

    main_window = MainWindow()
    main_window.show()

    app.exec()