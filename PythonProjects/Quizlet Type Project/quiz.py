#This file will be used for the 'quiz' feature or known on quizlet as Test

#Imports
from PyQt6.QtWidgets import (
    QWidget, QHBoxLayout, QVBoxLayout, 
    QLabel, QComboBox, QCheckBox, 
    QSpacerItem, QSizePolicy, QPushButton
)
from PyQt6.QtCore import Qt, QObject
from PyQt6.QtGui import QGuiApplication, QFont
from Sets import Sets
import random

#Quiz Class
class Quiz(QObject):
    #Constructor
    def __init__(self):
        #Parent constructor (for signals)
        super().__init__()

        #Variables that need to be global
        self.multiple_choice_questions = []
        self.matching_questions = []
        self.true_false_questions = []
        self.type_answer_questions = []
        
        self.gamemode = 0
        self.question_types = [True, True, True, True] #Multiple Choice, Matching, True/False, Type out Answers

    #-----------------------------------------------------------------
    # GUI Methods
    #-----------------------------------------------------------------
        
    #Main Container
    def genMainContainer(self):
        screen_resolution = QGuiApplication.primaryScreen().availableGeometry()
        width, height = screen_resolution.width(), screen_resolution.height()
        self.widthScale = width / 1920
        self.heightScale = height / 1032

        self.main_quiz_container = QWidget()
        container_layout = QHBoxLayout()
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

        self.start_up_container = self.genStartUpLayout()

        main_quiz_layout.addLayout(quiz_title_layout)
        main_quiz_layout.addSpacing(int(50 * self.heightScale))
        main_quiz_layout.addWidget(self.start_up_container)
        main_quiz_layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        container_layout.addSpacerItem(QSpacerItem(0, 0, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum))
        container_layout.addLayout(main_quiz_layout)
        container_layout.addSpacerItem(QSpacerItem(0, 0, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum))

        self.main_quiz_container.setLayout(container_layout)
        self.main_quiz_container.setHidden(True)

        return self.main_quiz_container

    #Start up layout (Includes settings and title)
    def genStartUpLayout(self):
        #Final Startup Layout
        start_up_container = QWidget()
        start_up_layout = QVBoxLayout()

        #Drop Downs
        drop_down_layout = QHBoxLayout()

        drop_down_font = QFont()
        drop_down_font.setPointSize(14)

        select_set_label = QLabel("Set: ")
        select_set_label.setFont(drop_down_font)
        self.select_set_dd = QComboBox()
        set_options = ['Set 1', 'Set 2'] #TEMP 
        self.select_set_dd.addItems(set_options)

        select_gamemode_label = QLabel("Gamemode: ")
        select_gamemode_label.setFont(drop_down_font)
        self.select_gamemode_dd = QComboBox()
        gamemode_options = ['Mixed', 'Given Definition, Enter Term', 'Given Term, Enter Definition']
        self.select_gamemode_dd.addItems(gamemode_options)

        drop_down_layout.addWidget(select_set_label)
        drop_down_layout.addWidget(self.select_set_dd)
        drop_down_layout.addSpacing(int(20 * self.widthScale))
        drop_down_layout.addWidget(select_gamemode_label)
        drop_down_layout.addWidget(self.select_gamemode_dd)
        drop_down_layout.setAlignment(Qt.AlignmentFlag.AlignLeft)

        #Question Types
        question_type_label_layout = QHBoxLayout()
        
        question_type_label = QLabel("Question Types")
        question_type_font = QFont()
        question_type_font.setPointSize(16)
        question_type_label.setFont(question_type_font)

        question_type_label_layout.addWidget(question_type_label)
        question_type_label_layout.setAlignment(Qt.AlignmentFlag.AlignHCenter)

        question_type_layouts = QVBoxLayout()

        multiple_choice_layout = QHBoxLayout()
        matching_layout = QHBoxLayout()
        true_false_layout = QHBoxLayout()
        type_answers_layout = QHBoxLayout()

        check_box_font = QFont()
        check_box_font.setPointSize(14)

        multiple_choice_cb = QCheckBox()
        multiple_choice_cb.setChecked(True)
        multiple_choice_label = QLabel("Multiple Choice")
        multiple_choice_label.setFont(check_box_font)

        matching_cb = QCheckBox()
        matching_cb.setChecked(True)
        matching_label = QLabel("Matching")
        matching_label.setFont(check_box_font)

        true_false_cb = QCheckBox()
        true_false_cb.setChecked(True)
        true_false_label = QLabel("True/False")
        true_false_label.setFont(check_box_font)

        type_answers_cb = QCheckBox()
        type_answers_cb.setChecked(True)
        type_answers_label = QLabel("Type out answers")
        type_answers_label.setFont(check_box_font)

        multiple_choice_layout.addWidget(multiple_choice_cb)
        multiple_choice_layout.addWidget(multiple_choice_label)
        multiple_choice_layout.setAlignment(Qt.AlignmentFlag.AlignLeft)
        
        matching_layout.addWidget(matching_cb)
        matching_layout.addWidget(matching_label)
        matching_layout.setAlignment(Qt.AlignmentFlag.AlignLeft)

        true_false_layout.addWidget(true_false_cb)
        true_false_layout.addWidget(true_false_label)
        true_false_layout.setAlignment(Qt.AlignmentFlag.AlignLeft)

        type_answers_layout.addWidget(type_answers_cb)
        type_answers_layout.addWidget(type_answers_label)
        type_answers_layout.setAlignment(Qt.AlignmentFlag.AlignLeft)

        question_type_layouts.addLayout(multiple_choice_layout)
        question_type_layouts.addLayout(matching_layout)
        question_type_layouts.addLayout(true_false_layout)
        question_type_layouts.addLayout(type_answers_layout)
        question_type_layouts.setAlignment(Qt.AlignmentFlag.AlignTop)

        #Start Game Button
        start_game_layout = QHBoxLayout()

        start_game_button = QPushButton("Start")
        start_game_button.setFixedSize(int(100 * self.widthScale), int(50 * self.heightScale))
        start_game_button.clicked.connect(self.startGame)

        start_game_layout.addWidget(start_game_button)
        start_up_layout.setAlignment(Qt.AlignmentFlag.AlignHCenter)

        start_up_layout.addLayout(drop_down_layout)
        start_up_layout.addSpacing(int(25 * self.heightScale))
        start_up_layout.addLayout(question_type_label_layout)
        start_up_layout.addLayout(question_type_layouts)
        start_up_layout.addSpacing(int(25 * self.heightScale))
        start_up_layout.addLayout(start_game_layout)
        start_up_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        start_up_container.setLayout(start_up_layout)
        return start_up_container
    
    #Show/Hide the main container
    def setHidden(self, status):
        self.main_quiz_container.setHidden(status)



    #----------------------------------------------------------
    # Main Game Methods
    #----------------------------------------------------------
        
    #Start the quiz game
    def startGame(self):
        pass

    
    #Populate Set Dropdown
    def populateSetDD(self):
        pass

    #Verify that the question type settings are valid
    def checkGameSettings(self):
        pass