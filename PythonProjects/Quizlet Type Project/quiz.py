#This file will be used for the 'quiz' feature or known on quizlet as Test

#Imports
from PyQt6.QtWidgets import (
    QWidget, QHBoxLayout, QVBoxLayout, 
    QLabel, QComboBox, QCheckBox, 
    QSpacerItem, QSizePolicy, QPushButton,
    QRadioButton, QLineEdit, QScrollArea
)
from PyQt6.QtCore import Qt, QObject
from PyQt6.QtGui import QGuiApplication, QFont
from Sets import Sets
import random
import math

class QuizQuestion:
    #Constructor
    def __init__(self, q, a):
        self.question = q
        self.answer = a

    #Getters
    def getQuestion(self):
        return self.question
    
    def getAnswer(self):
        return self.answer
    
    #Setters
    def setQuestion(self, q):
        self.question = q

    def setAnswer(self, a):
        self.answer = a

    #Randomize the question and answer for the mixed questions gamemode
    def randomize(self):
        doSwitch = random.randint(0, 1)
        if doSwitch == 0:
            temp = self.question
            self.question = self.answer
            self.answer = temp

#Class for storing data about a multiple choice question
class MultipleChoiceQuestion(QuizQuestion):
    #Constructor
    def __init__(self, q, a):
        super().__init__(q, a)

#Class for storing data about a matching question
class MatchingQuestion(QuizQuestion):
    #Constructor
    def __init__(self, q, a):
        super().__init__(q, a)

#Class for storing data about a true or false question
class TrueFalseQuestion(QuizQuestion):
    #Constructor
    def __init__(self, q, a):
        super().__init__(q, a)

#Class for storing data about a type answer question
class TypeAnswerQuestion(QuizQuestion):
    #Constructor
    def __init__(self, q, a):
        super().__init__(q, a)

#Class for storing data about

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

        self.question_types = []
        self.gamemode = 0

        #For getting set data
        self.set_data = Sets()

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
        self.checkGameSettings() #Check the first set in case it is less than 5 items

        self.main_game_scroll_area = QScrollArea()
        self.main_game_scroll_area.setWidgetResizable(True)

        self.main_game_scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOn)
        self.main_game_scroll_area.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Expanding)

        self.main_game_scroll_area.setFixedWidth(int(1250 * self.widthScale))

        main_game_container = self.genGameLayout()

        self.main_game_scroll_area.setWidget(main_game_container)
        self.main_game_scroll_area.setHidden(True)

        exit_game_layout = QHBoxLayout()

        self.exit_game_button = QPushButton("Cancel Game")
        self.exit_game_button.setFixedSize(int(125 * self.widthScale), int(50 * self.heightScale))
        self.exit_game_button.setHidden(True)
        self.exit_game_button.clicked.connect(self.cancelGame)

        exit_game_layout.addWidget(self.exit_game_button)
        exit_game_layout.setAlignment(Qt.AlignmentFlag.AlignLeft)

        main_quiz_layout.addLayout(quiz_title_layout)
        main_quiz_layout.addSpacing(int(50 * self.heightScale))
        main_quiz_layout.addWidget(self.start_up_container)
        main_quiz_layout.addWidget(self.main_game_scroll_area)
        main_quiz_layout.addLayout(exit_game_layout)
        main_quiz_layout.addSpacing(int(25 * self.heightScale))
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
        self.populateSetDD()
        self.select_set_dd.currentIndexChanged.connect(self.checkGameSettings)

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

        self.multiple_choice_cb = QCheckBox()
        self.multiple_choice_cb.setChecked(True)
        multiple_choice_label = QLabel("Multiple Choice")
        multiple_choice_label.setFont(check_box_font)

        self.matching_cb = QCheckBox()
        self.matching_cb.setChecked(True)
        matching_label = QLabel("Matching")
        matching_label.setFont(check_box_font)

        self.true_false_cb = QCheckBox()
        self.true_false_cb.setChecked(True)
        true_false_label = QLabel("True/False")
        true_false_label.setFont(check_box_font)

        self.type_answers_cb = QCheckBox()
        self.type_answers_cb.setChecked(True)
        type_answers_label = QLabel("Type out answers")
        type_answers_label.setFont(check_box_font)

        multiple_choice_layout.addWidget(self.multiple_choice_cb)
        multiple_choice_layout.addWidget(multiple_choice_label)
        multiple_choice_layout.setAlignment(Qt.AlignmentFlag.AlignLeft)
        
        matching_layout.addWidget(self.matching_cb)
        matching_layout.addWidget(matching_label)
        matching_layout.setAlignment(Qt.AlignmentFlag.AlignLeft)

        true_false_layout.addWidget(self.true_false_cb)
        true_false_layout.addWidget(true_false_label)
        true_false_layout.setAlignment(Qt.AlignmentFlag.AlignLeft)

        type_answers_layout.addWidget(self.type_answers_cb)
        type_answers_layout.addWidget(type_answers_label)
        type_answers_layout.setAlignment(Qt.AlignmentFlag.AlignLeft)

        question_type_layouts.addLayout(multiple_choice_layout)
        question_type_layouts.addLayout(matching_layout)
        question_type_layouts.addLayout(true_false_layout)
        question_type_layouts.addLayout(type_answers_layout)
        question_type_layouts.setAlignment(Qt.AlignmentFlag.AlignTop)

        #Start Game Button
        start_game_layout = QHBoxLayout()

        self.start_game_button = QPushButton("Start")
        self.start_game_button.setFixedSize(int(100 * self.widthScale), int(50 * self.heightScale))
        self.start_game_button.clicked.connect(self.startGame)

        self.error_label = QLabel("(*Minimum of 5 pairs is required for this game.)")
        self.error_label.setHidden(True)
        self.error_label.setFont(check_box_font)

        start_game_layout.addWidget(self.start_game_button)
        start_up_layout.setAlignment(Qt.AlignmentFlag.AlignHCenter)

        start_up_layout.addLayout(drop_down_layout)
        start_up_layout.addSpacing(int(25 * self.heightScale))
        start_up_layout.addLayout(question_type_label_layout)
        start_up_layout.addLayout(question_type_layouts)
        start_up_layout.addSpacing(int(25 * self.heightScale))
        start_up_layout.addLayout(start_game_layout)
        start_up_layout.addWidget(self.error_label)
        start_up_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        start_up_container.setLayout(start_up_layout)
        return start_up_container
    
    #Generate Layout Container where all questions will be stored
    def genGameLayout(self):
        main_game_container = QWidget()
        main_game_layout = QVBoxLayout()

        #Questions Layouts
        self.multiple_choice_questions_layout = QVBoxLayout()
        self.matching_questions_layout = QVBoxLayout()
        self.true_false_questions_layout = QVBoxLayout()
        self.type_answer_questions_layout = QVBoxLayout()

        #Sub Titles
        sub_title_font = QFont()
        sub_title_font.setPointSize(18)
        sub_title_font.setBold(True)

        self.mc_sub_title_container = QWidget()
        self.ma_sub_title_container = QWidget()
        self.tf_sub_title_container = QWidget()
        self.ta_sub_title_container = QWidget()

        mc_sub_title_layout = QVBoxLayout()
        ma_sub_title_layout = QVBoxLayout()
        tf_sub_title_layout = QVBoxLayout()
        ta_sub_title_layout = QVBoxLayout()

        self.multiple_choice_sub_title = QLabel("Multiple Choice")
        self.matching_sub_title = QLabel("Matching")
        self.true_false_sub_title = QLabel("True or False")
        self.type_answer_sub_title = QLabel("Type Answers")

        self.multiple_choice_sub_title.setFont(sub_title_font)
        self.matching_sub_title.setFont(sub_title_font)
        self.true_false_sub_title.setFont(sub_title_font)
        self.type_answer_sub_title.setFont(sub_title_font)

        mc_sub_title_layout.addWidget(self.multiple_choice_sub_title)
        ma_sub_title_layout.addWidget(self.matching_sub_title)
        tf_sub_title_layout.addWidget(self.true_false_sub_title)
        ta_sub_title_layout.addWidget(self.type_answer_sub_title)

        mc_sub_title_layout.addSpacing(int(10 * self.heightScale))
        ma_sub_title_layout.addSpacing(int(10 * self.heightScale))
        tf_sub_title_layout.addSpacing(int(10 * self.heightScale))
        ta_sub_title_layout.addSpacing(int(10 * self.heightScale))

        mc_sub_title_layout.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        ma_sub_title_layout.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        tf_sub_title_layout.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        ta_sub_title_layout.setAlignment(Qt.AlignmentFlag.AlignHCenter)

        self.mc_sub_title_container.setLayout(mc_sub_title_layout)
        self.ma_sub_title_container.setLayout(ma_sub_title_layout)
        self.tf_sub_title_container.setLayout(tf_sub_title_layout)
        self.ta_sub_title_container.setLayout(ta_sub_title_layout)

        submit_answers_layout = QHBoxLayout()
        
        submit_answers_button = QPushButton("Submit")
        submit_answers_button.setFixedSize(int(100 * self.widthScale), int(50 * self.heightScale))

        submit_answers_layout.addWidget(submit_answers_button)
        submit_answers_layout.setAlignment(Qt.AlignmentFlag.AlignHCenter)

        main_game_layout.addWidget(self.mc_sub_title_container)
        main_game_layout.addLayout(self.multiple_choice_questions_layout)
        main_game_layout.addWidget(self.ma_sub_title_container)
        main_game_layout.addLayout(self.matching_questions_layout)
        main_game_layout.addWidget(self.tf_sub_title_container)
        main_game_layout.addLayout(self.true_false_questions_layout)
        main_game_layout.addWidget(self.ta_sub_title_container)
        main_game_layout.addLayout(self.type_answer_questions_layout)
        main_game_layout.addSpacing(int(25 * self.heightScale))
        main_game_layout.addLayout(submit_answers_layout)
        main_game_layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        main_game_container.setLayout(main_game_layout)
        return main_game_container
    
    #Add a multiple choice question
    def addMultipleChoiceQuestion(self):
        main_mc_layout = QVBoxLayout()

        question_layout = QHBoxLayout()

        question_label = QLabel("Sample Question")
        question_font = QFont()
        question_font.setPointSize(14)
        question_label.setFont(question_font)

        question_layout.addWidget(question_label)
        question_layout.setAlignment(Qt.AlignmentFlag.AlignHCenter)

        radio_button_container = QWidget()
        radio_button_space_layout = QHBoxLayout()
        radio_button_layout = QVBoxLayout()
        radio_buttons = []
        for i in range(4):
            new_button = QRadioButton("Sample {}".format(i + 1))
            radio_button_layout.addWidget(new_button)
            new_button.setParent(radio_button_container)
            radio_buttons.append(new_button)

        radio_button_space_layout.addSpacing(int(400 * self.widthScale))
        radio_button_space_layout.addLayout(radio_button_layout)
        radio_button_space_layout.setAlignment(Qt.AlignmentFlag.AlignLeft)
        radio_button_container.setLayout(radio_button_space_layout)

        main_mc_layout.addLayout(question_layout)
        main_mc_layout.addWidget(radio_button_container)
        main_mc_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        
        self.multiple_choice_questions_layout.addLayout(main_mc_layout)
        self.multiple_choice_questions_layout.addSpacing(int(25 * self.heightScale))

    #Add a matching question
    def addMatchingQuestion(self):
        main_matching_layout = QHBoxLayout()

        matching_input = QLineEdit()
        matching_input.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        matching_input.setFixedSize(int(50 * self.widthScale), int(25 * self.heightScale))
        
        question_font = QFont()
        question_font.setPointSize(14)

        matching_input_label = QLabel("Sample Question")
        matching_input_label.setFont(question_font)

        matching_answer_label = QLabel("A: Sample Answer")
        matching_answer_label.setFont(question_font)

        main_matching_layout.addSpacing(int(200 * self.widthScale))
        main_matching_layout.addWidget(matching_input)
        main_matching_layout.addWidget(matching_input_label)
        main_matching_layout.addSpacerItem(QSpacerItem(0, 0, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed))
        main_matching_layout.addWidget(matching_answer_label)
        main_matching_layout.addSpacing(int(200 * self.widthScale))
        main_matching_layout.setAlignment(Qt.AlignmentFlag.AlignLeft)
        
        self.matching_questions_layout.addLayout(main_matching_layout)
        self.matching_questions_layout.addSpacing(int(25 * self.heightScale))

    #Add a true or false question
    def addTrueFalseQuestion(self):
        main_true_false_layout = QVBoxLayout()

        true_false_question_layout = QHBoxLayout()

        true_false_question_label = QLabel("Sample True or False")
        true_false_question_font = QFont()
        true_false_question_font.setPointSize(14)
        true_false_question_label.setFont(true_false_question_font)

        true_false_question_layout.addWidget(true_false_question_label)
        true_false_question_layout.setAlignment(Qt.AlignmentFlag.AlignHCenter)

        true_false_options_container = QWidget()
        true_false_space_layout = QHBoxLayout()
        true_false_options_layout = QVBoxLayout()

        true_button = QRadioButton("True")
        false_button = QRadioButton("False")

        true_button.setParent(true_false_options_container)
        false_button.setParent(true_false_options_container)

        true_false_options_layout.addWidget(true_button)
        true_false_options_layout.addWidget(false_button)

        true_false_space_layout.addSpacing(int(400 * self.widthScale))
        true_false_space_layout.addLayout(true_false_options_layout)
        true_false_space_layout.setAlignment(Qt.AlignmentFlag.AlignLeft)
        true_false_options_container.setLayout(true_false_space_layout)

        main_true_false_layout.addLayout(true_false_question_layout)
        main_true_false_layout.addWidget(true_false_options_container)
        main_true_false_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        
        self.true_false_questions_layout.addLayout(main_true_false_layout)
        self.true_false_questions_layout.addSpacing(int(25 * self.heightScale))

    #Add a type answer question
    def addTypeAnswerQuestion(self):
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
        main_type_answer_input.setFixedWidth(int(600 * self.widthScale))

        main_type_answer_input_layout.addSpacerItem(QSpacerItem(0, 0, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum))
        main_type_answer_input_layout.addWidget(main_type_answer_input)
        main_type_answer_input_layout.addSpacerItem(QSpacerItem(0, 0, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum))

        main_type_answer_layout.addLayout(main_type_answer_label_layout)
        main_type_answer_layout.addLayout(main_type_answer_input_layout)
        main_type_answer_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        
        self.type_answer_questions_layout.addLayout(main_type_answer_layout)
        self.type_answer_questions_layout.addSpacing(int(25 * self.heightScale))

    #Show/Hide the main container
    def setHidden(self, status):
        self.main_quiz_container.setHidden(status)



    #----------------------------------------------------------
    # Main Game Methods
    #----------------------------------------------------------
        
    #Start the quiz game
    def startGame(self):
        self.start_up_container.setHidden(True)
        self.main_game_scroll_area.setHidden(False)
        self.exit_game_button.setHidden(False)

        #Pull data from startup menu
        self.set_index = self.select_set_dd.currentIndex()
        self.gamemode = self.select_gamemode_dd.currentIndex() #0-Mixed 1-Given Definition 2- Given Term
        self.question_types = [self.multiple_choice_cb.isChecked(), self.matching_cb.isChecked(), self.true_false_cb.isChecked(), self.type_answers_cb.isChecked()]

        #Get Set Data
        set_title = self.set_data.getSetTitle(self.set_index)
        set_content = self.set_data.getSetContent(set_title)
        
        #Figure out how many of each question type should be generated
        divisor = self.question_types.count(True)
        num_per_question_type = math.floor(len(set_content) / divisor)
        num_extra_questions = len(set_content) % divisor

        num_mc, num_ma, num_tf, num_ta = 0,0,0,0

        #Check multiple choice first since I chose a stupid order
        if self.question_types[0]:
            self.mc_sub_title_container.setHidden(False)
            num_mc = num_per_question_type
            if (self.question_types[1] and num_extra_questions > 1) or (not(self.question_types[1]) and num_extra_questions > 0): #Add extra question to mc if conditions are right
                num_mc += 1
                num_extra_questions -= 1
        else:
            self.mc_sub_title_container.setHidden(True)
            
        if self.question_types[1]:
            self.ma_sub_title_container.setHidden(False)
            num_ma = num_per_question_type
            if num_extra_questions > 0:
                num_ma += 1
                num_extra_questions -= 1
        else:
            self.ma_sub_title_container.setHidden(True)

        if self.question_types[2]:
            self.tf_sub_title_container.setHidden(False)
            num_tf = num_per_question_type
            if num_extra_questions:
                num_tf += 1
                num_extra_questions -= 1
        else:
            self.tf_sub_title_container.setHidden(True)

        if self.question_types[3]:
            self.ta_sub_title_container.setHidden(False)
            num_ta = num_per_question_type
        else:
            self.ta_sub_title_container.setHidden(True)

        #Create Questions
        for mc in range(num_mc):
            self.addMultipleChoiceQuestion()

        for ma in range(num_ma):
            self.addMatchingQuestion()

        for tf in range(num_tf):
            self.addTrueFalseQuestion()

        for ta in range(num_ta):
            self.addTypeAnswerQuestion()



    #Populate Set Dropdown
    def populateSetDD(self):
        set_titles = self.set_data.getAllSetTitles()
        self.select_set_dd.addItems(set_titles)

    #Verify that the question type settings are valid
    def checkGameSettings(self):
        #Get data of set current selected in the drop down
        current_set_index = self.select_set_dd.currentIndex()
        current_set_title = self.set_data.getSetTitle(current_set_index)
        current_set_data = self.set_data.getSetContent(current_set_title)

        if len(current_set_data) <= 4:
            self.start_game_button.setEnabled(False)
            self.error_label.setHidden(False)
        else:
            self.start_game_button.setEnabled(True)
            self.error_label.setHidden(True)

    #Cancel Game
    def cancelGame(self):
        self.main_game_scroll_area.setHidden(True)
        self.exit_game_button.setHidden(True)
        self.start_up_container.setHidden(False)
        
    #Reset Game
    def resetGame(self):
        self.clearQuestions()

        self.multiple_choice_questions = []
        self.matching_questions = []
        self.true_false_questions = []
        self.type_answer_questions = []
    
        self.gamemode = 0

    #Clear all questions from the scroll area
    def clearQuestions(self):
        pass
        
        