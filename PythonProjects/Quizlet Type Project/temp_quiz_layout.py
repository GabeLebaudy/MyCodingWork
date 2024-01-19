#This file is temporary, will be used to generate all layouts for the test functionality 


#Imports
from PyQt6.QtWidgets import (
    QMainWindow, QApplication, QWidget,
    QHBoxLayout, QVBoxLayout, QLabel,
    QComboBox, QCheckBox, QRadioButton,
    QLineEdit, QSizePolicy, QSpacerItem
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QGuiApplication, QFont

#Main window class (Will remove in main app)
class MainWindow(QMainWindow):
    #Constructor
    def __init__(self):
        super().__init__()

        screen_resolution = QGuiApplication.primaryScreen().availableGeometry()
        width, height = screen_resolution.width(), screen_resolution.height()
        self.widthScale = width / 1920
        self.heightScale = height / 1032

        self.main_quiz_container = QWidget()
        main_quiz_layout = QVBoxLayout()

        #Title Label
        quiz_title_layout = QHBoxLayout()

        quiz_title_label = QLabel("Quiz!")
        quiz_title_font = QFont()
        quiz_title_font.setPointSize(24)
        quiz_title_font.setBold(True)
        quiz_title_label.setFont(quiz_title_font)

        quiz_title_layout.addWidget(quiz_title_label)
        quiz_title_layout.setAlignment(Qt.AlignmentFlag.AlignHCenter)

        mc_1 = self.genMultipleChoiceQuestion()
        mc_2 = self.genMultipleChoiceQuestion()

        ma_1 = self.genMatchingQuestion()
        ma_2 = self.genMatchingQuestion()

        tf_1 = self.genTrueFalseQuestion()
        tf_2 = self.genTrueFalseQuestion()

        ta_1 = self.genTypeAnswerQuestion()
        ta_2 = self.genTypeAnswerQuestion()

        main_quiz_layout.addLayout(quiz_title_layout)
        main_quiz_layout.addSpacing(int(50 * self.heightScale))
        main_quiz_layout.addLayout(mc_1)
        main_quiz_layout.addSpacing(int(20 * self.heightScale))
        main_quiz_layout.addLayout(mc_2)
        main_quiz_layout.addSpacing(int(20 * self.heightScale))
        main_quiz_layout.addLayout(ma_1)
        main_quiz_layout.addSpacing(int(10 * self.heightScale))
        main_quiz_layout.addLayout(ma_2)
        main_quiz_layout.addSpacing(int(20 * self.heightScale))
        main_quiz_layout.addLayout(tf_1)
        main_quiz_layout.addSpacing(int(10 * self.heightScale))
        main_quiz_layout.addLayout(tf_2)
        main_quiz_layout.addSpacing(int(20 * self.heightScale))
        main_quiz_layout.addLayout(ta_1)
        main_quiz_layout.addSpacing(int(20 * self.heightScale))
        main_quiz_layout.addLayout(ta_2)
        main_quiz_layout.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignHCenter)
        self.main_quiz_container.setLayout(main_quiz_layout)

        self.setCentralWidget(self.main_quiz_container)

    #Multiple Choice Question
    def genMultipleChoiceQuestion(self):
        main_mc_layout = QVBoxLayout()

        question_layout = QHBoxLayout()

        question_label = QLabel("Sample Question")
        question_font = QFont()
        question_font.setPointSize(14)
        question_label.setFont(question_font)

        question_layout.addWidget(question_label)
        question_layout.setAlignment(Qt.AlignmentFlag.AlignHCenter)

        radio_button_container = QWidget()
        radio_button_layout = QVBoxLayout()
        radio_buttons = []
        for i in range(4):
            new_button = QRadioButton("Sample {}".format(i + 1))
            radio_button_layout.addWidget(new_button)
            new_button.setParent(radio_button_container)
            radio_buttons.append(new_button)

        radio_button_layout.setAlignment(Qt.AlignmentFlag.AlignLeft)
        radio_button_container.setLayout(radio_button_layout)

        main_mc_layout.addLayout(question_layout)
        main_mc_layout.addWidget(radio_button_container)
        main_mc_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        return main_mc_layout

    #Matching Question
    def genMatchingQuestion(self):
        main_matching_layout = QHBoxLayout()

        matching_input = QLineEdit()
        matching_input.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        matching_input.setFixedSize(int(50 * self.widthScale), int(25 * self.heightScale))
        matching_input_label = QLabel("Sample Question")

        matching_answer_label = QLabel("A: Sample Answer")

        main_matching_layout.addWidget(matching_input)
        main_matching_layout.addWidget(matching_input_label)
        main_matching_layout.addSpacing(int(200 * self.widthScale))
        main_matching_layout.addWidget(matching_answer_label)
        main_matching_layout.setAlignment(Qt.AlignmentFlag.AlignLeft)
        return main_matching_layout

    #True or False Question
    def genTrueFalseQuestion(self):
        main_true_false_layout = QVBoxLayout()

        true_false_question_layout = QHBoxLayout()

        true_false_question_label = QLabel("Sample True or False")
        true_false_question_font = QFont()
        true_false_question_font.setPointSize(14)
        true_false_question_label.setFont(true_false_question_font)

        true_false_question_layout.addWidget(true_false_question_label)
        true_false_question_layout.setAlignment(Qt.AlignmentFlag.AlignHCenter)

        true_false_options_container = QWidget()
        true_false_options_layout = QVBoxLayout()

        true_button = QRadioButton("True")
        false_button = QRadioButton("False")

        true_button.setParent(true_false_options_container)
        false_button.setParent(true_false_options_container)

        true_false_options_layout.addWidget(true_button)
        true_false_options_layout.addWidget(false_button)
        true_false_options_layout.setAlignment(Qt.AlignmentFlag.AlignLeft)
        true_false_options_container.setLayout(true_false_options_layout)

        main_true_false_layout.addLayout(true_false_question_layout)
        main_true_false_layout.addWidget(true_false_options_container)
        main_true_false_layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        return main_true_false_layout

    #Type out answer question
    def genTypeAnswerQuestion(self):
        main_type_answer_layout = QVBoxLayout()

        main_type_answer_label_layout = QHBoxLayout()

        main_type_answer_label = QLabel("Sample Type Answer Question")
        main_type_answer_font = QFont()
        main_type_answer_font.setPointSize(14)
        main_type_answer_label.setFont(main_type_answer_font)

        main_type_answer_label_layout.addWidget(main_type_answer_label)
        main_type_answer_label_layout.setAlignment(Qt.AlignmentFlag.AlignHCenter)

        main_type_answer_input_layout = QHBoxLayout()

        main_type_answer_input = QLineEdit()
        main_type_answer_input.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        main_type_answer_input.setFixedWidth(int(200 * self.widthScale))

        main_type_answer_input_layout.addSpacerItem(QSpacerItem(0, 0, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum))
        main_type_answer_input_layout.addWidget(main_type_answer_input)
        main_type_answer_input_layout.addSpacerItem(QSpacerItem(0, 0, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum))

        main_type_answer_layout.addLayout(main_type_answer_label_layout)
        main_type_answer_layout.addLayout(main_type_answer_input_layout)
        main_type_answer_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        return main_type_answer_layout

#Main Method
if __name__ == "__main__":
    app = QApplication([])

    window = MainWindow()
    window.show()

    app.exec()