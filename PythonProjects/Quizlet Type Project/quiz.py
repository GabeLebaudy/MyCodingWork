#This file will be used for the 'quiz' feature or known on quizlet as Test

#Imports
from PyQt6.QtWidgets import (
    QWidget, QHBoxLayout, QVBoxLayout, 
    QLabel, QComboBox, QCheckBox, 
    QSpacerItem, QSizePolicy, QPushButton,
    QRadioButton, QLineEdit, QScrollArea,
    QSpinBox, QAbstractSpinBox
)
from PyQt6.QtCore import Qt, QObject, pyqtSignal
from PyQt6.QtGui import QGuiApplication, QFont
from Sets import Sets
import random
import math
import re

class QuizQuestion:
    #Constructor
    def __init__(self):
        self.question = None
        self.answer = None

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
        return doSwitch

#Class for storing data about a multiple choice question
class MultipleChoiceQuestion(QuizQuestion):
    #Constructor
    def __init__(self, main_layout, q_layout, q_label, btn_container, btn_layout, btn_list, button_labels, button_layouts):
        super().__init__()
        self.main_layout = main_layout
        self.question_layout = q_layout
        self.question_label = q_label
        self.button_container = btn_container
        self.button_layout = btn_layout
        self.button_list = btn_list
        self.button_text_layouts = button_layouts
        self.button_labels = button_labels

        self.correct_answer_index = 0
    
    #Set the question and answer properties of the parent object, then set the question label accordingly
    def setQuestionAndAnswer(self, q, a, gamemode):
        #Set question and answer in parent object
        super().setQuestion(q)
        super().setAnswer(a)

        #Check if the user wants to randomize the question
        if gamemode == 0:
            didSwitch = super().randomize() #Initially definition will always be question, if it did switch, the term is the question
            if didSwitch == 0: #The term is the question, and definition is the answer
                self.question_label.setText("What is the definition of {}?".format(super().getQuestion()))
            else: #Did not switch, definition is the question
                self.question_label.setText("What term is defined by {}?".format(super().getQuestion()))

        if gamemode == 1: #Definition is question
            self.question_label.setText("What is the definition of {}?".format(q))

        if gamemode == 2: #Term is question
            self.question_label.setText("What term is defined by {}?".format(q))

        self.question_label.setFixedHeight(self.question_label.sizeHint().height())

    #Get current answer
    def getAnswer(self):
        return super().getAnswer()

    #Set the answers
    def setAnswerOptions(self, all_answers):
        #Store the index of the radio button with the correct answer
        self.correct_answer_index = random.randint(0, 3)

        #Find 3 answers that are not the same, and are not the correct answer
        answer_sub_ind = all_answers.index(super().getAnswer())

        incorrect_answers = []
        while not incorrect_answers or answer_sub_ind in incorrect_answers:
            incorrect_answers = random.sample(range(len(all_answers)), 3)

        #Set the text of each radio button
        for i in range(4):
            if i == self.correct_answer_index: #Correct radio button answer
                self.button_labels[i].setText(super().getAnswer())
                #self.button_labels[i].setFixedHeight(self.button_labels[i].sizeHint().height())
            else:
                ind = incorrect_answers.pop(0)
                self.button_labels[i].setText(all_answers[ind])
                #self.button_labels[i].setFixedHeight(self.button_labels[i].sizeHint().height())

    #Check if an answer was selected
    def isAnswered(self):
        for btn in self.button_list:
            if btn.isChecked():
                return True
        return False
    
    #Check if answer selected was correct or not
    def checkAnswer(self):
        isCorrect = False
        for i in range(len(self.button_list)):
            if self.button_list[i].isChecked():
                if i == self.correct_answer_index:
                    current_text = self.button_list[i].text()
                    self.button_list[i].setText("{} (Correct)".format(current_text))
                    isCorrect = True
                else:
                    current_text = self.button_list[i].text()
                    self.button_list[i].setText("{} (Incorrect)".format(current_text))
                    current_text = self.button_list[self.correct_answer_index].text()
                    self.button_list[self.correct_answer_index].setText("{} (Correct)".format(current_text))
                    
            self.button_list[i].setEnabled(False)
            
        return isCorrect
        

    #Delete the question (On restart and game end)
    def deleteQuestion(self):
        #Start from bottom of the layouts, and remove upward
        for label in self.button_labels:
            label.deleteLater()

        for btn in self.button_list:
            btn.deleteLater()

        for layout in self.button_text_layouts:
            layout.deleteLater()

        self.button_layout.deleteLater()
        self.button_container.deleteLater()
        self.question_label.deleteLater()
        self.question_layout.deleteLater()
        self.main_layout.deleteLater()

#Class for storing data about a matching question
class MatchingQuestion(QuizQuestion):
    #Constructor
    def __init__(self, container, main_layout, input_field, input_label, answer_label, reveal_layout, reveal_label):
        super().__init__()
        self.container = container
        self.main_layout = main_layout
        self.input_field = input_field
        self.input_label = input_label
        self.answer_label = answer_label
        self.reveal_layout = reveal_layout
        self.reveal_label = reveal_label
        
        self.ans_letter = 'a'
        self.corresponding_answer = 0

    #Set question and answer in parent layout and question label
    def setQuestionAndAnswer(self, q, a, gamemode):
        #Set question and answer in parent object
        super().setQuestion(q)
        super().setAnswer(a)

        #Depending on gamemode, set questions accordingly
        if gamemode == 0:
            didSwitch = super().randomize() #Initially definition will always be question, if it did switch, the term is the question
            if didSwitch == 0: #The term is the question, and definition is the answer
                self.input_label.setText(super().getQuestion())
            else: #Did not switch, definition is the question
                self.input_label.setText(super().getQuestion())

        if gamemode == 1: #Definition is question
            self.input_label.setText(q)

        if gamemode == 2: #Term is question
            self.input_label.setText(q)

    #Get current answer
    def getAnswer(self):
        return super().getAnswer()
    
    #Get the answer on the label
    def getCorrespondingAnswer(self):
        return self.corresponding_answer
    
    #Set the corresponding answer, and store index for checking the answer
    def setAnswerLabel(self, loop_index, matching_answers):
        #Generate a letter for the current line
        self.ans_letter = self.genLetter(loop_index)

        #Generate answer to add to label
        ans_ind = random.randint(0, len(matching_answers) - 1)
        self.corresponding_answer = matching_answers[ans_ind]

        #Set the answer label
        self.answer_label.setText("{}: {}".format(self.ans_letter, self.corresponding_answer))
        return ans_ind #To remove to ensure that it won't be used twice
    
    #Generate the subsequent lettering scheme
    def genLetter(self, ind):
        doMultipleLetters = (math.floor(ind / 26) > 0)
        if not doMultipleLetters: #Single Letter
            letter = chr(97 + ind)
            return letter
        else: #Two letters
            first_ind = math.floor(ind / 26)
            second_ind = ind % 26

            first_letter = chr(96 + first_ind)
            second_letter = chr(97 + second_ind)
            return first_letter + second_letter

    #Check if question is answered
    def isAnswered(self):
        answer = self.input_field.text()
        if not answer:
            return False
        return True
    
    #Find the index of the question that contains the answer selcted in the input field
    def findLetterIndex(self):
        user_answer = self.input_field.text().strip()
        #Invalid index
        if len(user_answer) > 2:
            self.showCorrectAnswer()
            return False
        
        #Check to ensure all characters
        pattern = re.compile(r'^[a-z]+$')
        if not bool(pattern.match(user_answer)):
            self.showCorrectAnswer()
            return False
        
        #Find index of question that has answer selected
        return self.letterToInd(user_answer.lower())
    
    #Check answer
    def checkAnswer(self, answer):
        isCorrect = False
        if super().getAnswer() == answer:
            self.reveal_label.setText("Correct")
            self.reveal_label.setHidden(False)
            isCorrect = True
        else:
            self.showCorrectAnswer()
        
        self.input_field.setReadOnly(True)
        return isCorrect

    def letterToInd(self, answer):
        if len(answer) == 1:
            return ord(answer) - 97
        else:
            return (ord(answer[0]) - 96) * 26 + (ord(answer[1]) - 97)
        
    def showCorrectAnswer(self):
        self.reveal_label.setText("Incorrect. Correct answer: {}".format(super().getAnswer()))
        self.reveal_label.setHidden(False)

    #Delete the question
    def deleteQuestion(self):
        self.reveal_label.deleteLater()
        self.reveal_layout.deleteLater()
        self.answer_label.deleteLater()
        self.input_label.deleteLater()
        self.input_field.deleteLater()
        self.main_layout.deleteLater()
        self.container.deleteLater()

#Class for storing data about a true or false question
class TrueFalseQuestion(QuizQuestion):
    #Constructor
    def __init__(self, main_layout, question_layout, question_label, answer_container, answer_space_layout, answer_layout, true_button, false_button):
        super().__init__()
        self.main_layout = main_layout
        self.question_layout = question_layout
        self.question_label = question_label
        self.answer_container = answer_container
        self.answer_space_layout = answer_space_layout
        self.answer_layout = answer_layout
        self.true_button = true_button
        self.false_button = false_button

        self.true_false_answer = True
    
    #Set question and answer of parent container
    def setQuestionAndAnswer(self, q, a, gamemode):
        #Set properties of parent layout
        super().setQuestion(q)
        super().setAnswer(a)

        #If user selected mixed, randomize question and answer
        if gamemode == 0:
            self.didSwitch = super().randomize()

    #Get current answer
    def getAnswer(self):
        return super().getAnswer()
    
    #Set question label
    def setQuestionLabel(self, all_terms, all_defs, gamemode):
        #Randomly select if the answer is true or false
        self.true_false_answer = random.choice([True, False])

        #Set the text of the label based on the gamemode
        if gamemode == 0:
            if self.true_false_answer: #Answer is true
                if self.didSwitch == 0: #Term is the question
                    self.question_label.setText("The definition of {} is {}.".format(super().getQuestion(), super().getAnswer()))
                else: #Definition is the question
                    self.question_label.setText("{} defines the term {}.".format(super().getQuestion(), super().getAnswer()))

            else: #Answer is false
                if self.didSwitch == 0: #Term is question
                    #Find random false definition
                    wrong_answer = self.getWrongAnswer(all_defs)
                    self.question_label.setText("The definition of {} is {}.".format(super().getQuestion(), wrong_answer))
                else: #Definition is question
                    #Find random false term
                    wrong_answer = self.getWrongAnswer(all_terms)
                    self.question_label.setText("{} defines the term {}.".format(super().getQuestion(), wrong_answer))

        if gamemode == 1: #Definition is the question
            if self.true_false_answer:
                self.question_label.setText("The definition of {} is {}.".format(super().getQuestion(), super().getAnswer()))
            else:
                #Find random false term
                wrong_answer = self.getWrongAnswer(all_terms)

                self.question_label.setText("The definition of {} is {}.".format(super().getQuestion(), wrong_answer))

        if gamemode == 2: #Term is the question
            if self.true_false_answer:
                self.question_label.setText("{} defines the term {}.".format(super().getQuestion(), super().getAnswer()))
            else:
                #Find random false definition 
                wrong_answer = self.getWrongAnswer(all_defs)

                self.question_label.setText("{} defines the term {}.".format(super().getQuestion(), wrong_answer))

        self.question_label.setFixedHeight(self.question_label.sizeHint().height())
                
    #Get a random wrong answer
    def getWrongAnswer(self, answers):
        correct_answer_ind = answers.index(super().getAnswer())

        wrong_ind = -1
        while wrong_ind < 0 or wrong_ind == correct_answer_ind:
            wrong_ind = random.randint(0, len(answers) - 1)
        
        return answers[wrong_ind]
    
    #Check if question is answered
    def isAnswered(self):
        if not self.true_button.isChecked() and not self.false_button.isChecked():
            return False
        return True
    
    #Check answer
    def checkAnswer(self):
        isCorrect = False
        if self.true_false_answer:
            if self.true_button.isChecked():
                isCorrect = True
                self.true_button.setText("True (Correct)")
            else:
                self.true_button.setText("True (Incorrect)")
                self.false_button.setText("False (Correct)")
        else:
            if self.false_button.isChecked():
                isCorrect = True
                self.false_button.setText("False (Correct)")
            else:
                self.true_button.setText("True (Incorrect)")
                self.false_button.setText("False (Correct)")
                
        self.true_button.setEnabled(False)
        self.false_button.setEnabled(False)
        return isCorrect

    
    #Delete the question
    def deleteQuestion(self):
        self.false_button.deleteLater()
        self.true_button.deleteLater()
        self.answer_layout.deleteLater()
        self.answer_space_layout.deleteLater()
        self.answer_container.deleteLater()
        self.question_label.deleteLater()
        self.question_layout.deleteLater()
        self.main_layout.deleteLater()

#Class for storing data about a type answer question
class TypeAnswerQuestion(QuizQuestion):
    #Constructor
    def __init__(self, main_layout, label_layout, question_label, input_layout, answer_input, answer_display_layout, answer_display_label):
        super().__init__()
        self.main_layout = main_layout
        self.label_layout = label_layout
        self.question_label = question_label
        self.input_layout = input_layout
        self.answer_input = answer_input
        self.answer_display_layout = answer_display_layout
        self.answer_display_label = answer_display_label

    #Set question and answer properties of parent object and set the question label
    def setQuestionAndAnswer(self, q, a, gamemode):
        #Set parent properties
        super().setQuestion(q)
        super().setAnswer(a)

        #Use user selected gamemode to determine question label's text
        #Check if the user wants to randomize the question
        if gamemode == 0:
            didSwitch = super().randomize() #Initially definition will always be question, if it did switch, the term is the question
            if didSwitch == 0: #The term is the question, and definition is the answer
                self.question_label.setText("What is the definition of {}?".format(super().getQuestion()))
            else: #Did not switch, definition is the question
                self.question_label.setText("What term is defined by {}?".format(super().getQuestion()))

        if gamemode == 1: #Definition is question
            self.question_label.setText("What is the definition of {}?".format(q))

        if gamemode == 2: #Term is question
            self.question_label.setText("What term is defined by {}?".format(q))

        self.question_label.setFixedHeight(self.question_label.sizeHint().height())
        
    #Get current answer
    def getAnswer(self):
        return super().getAnswer()
    
    #Check if question is answered
    def isAnswered(self):
        answer = self.answer_input.text()
        if not answer:
            return False
        return True
    
    #Check if answer is correct
    def checkAnswer(self):
        isCorrect = False
        user_answer = self.answer_input.text()
        if user_answer.lower() == super().getAnswer().lower():
            isCorrect = True
            self.answer_display_label.setText("Correct")
            self.answer_display_label.setHidden(False)
        else:
            self.answer_display_label.setText("Incorrect. Correct answer: {}".format(super().getAnswer()))
            self.answer_display_label.setHidden(False)
            
        
        self.answer_input.setReadOnly(True)
        return isCorrect

    #Delete the question
    def deleteQuestion(self):
        self.answer_display_label.deleteLater()
        self.answer_display_layout.deleteLater()
        self.answer_input.deleteLater()
        self.input_layout.deleteLater()
        self.question_label.deleteLater()
        self.label_layout.deleteLater()
        self.main_layout.deleteLater()
    
#Quiz Class
class Quiz(QObject):

    #Prompt a message from main window
    message_signal = pyqtSignal(list)

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
        self.all_answers = []
        self.matching_answers = []

        #For True/False Questions
        self.all_terms = []
        self.all_defs = []

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
        self.select_set_dd.setFixedSize(int(200 * self.widthScale), int(30 * self.heightScale))
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
        
        question_type_label = QLabel("Question Options")
        question_type_font = QFont()
        question_type_font.setPointSize(16)
        question_type_label.setFont(question_type_font)

        question_type_label_layout.addWidget(question_type_label)
        question_type_label_layout.setAlignment(Qt.AlignmentFlag.AlignHCenter)

        question_type_layouts = QVBoxLayout()

        check_box_font = QFont()
        check_box_font.setPointSize(14)

        self.multiple_choice_cb = QCheckBox("Multiple Choice")
        self.multiple_choice_cb.setChecked(True)
        self.multiple_choice_cb.setFont(check_box_font)
        self.multiple_choice_cb.clicked.connect(self.checkGameSettings)

        self.matching_cb = QCheckBox("Matching")
        self.matching_cb.setChecked(True)
        self.matching_cb.setFont(check_box_font)
        self.matching_cb.clicked.connect(self.checkGameSettings)

        self.true_false_cb = QCheckBox("True/False")
        self.true_false_cb.setChecked(True)
        self.true_false_cb.setFont(check_box_font)
        self.true_false_cb.clicked.connect(self.checkGameSettings)

        self.type_answers_cb = QCheckBox("Type out answers")
        self.type_answers_cb.setChecked(True)
        self.type_answers_cb.setFont(check_box_font)
        self.type_answers_cb.clicked.connect(self.checkGameSettings)

        question_type_layouts.addWidget(self.multiple_choice_cb)
        question_type_layouts.addWidget(self.matching_cb)
        question_type_layouts.addWidget(self.true_false_cb)
        question_type_layouts.addWidget(self.type_answers_cb)
        question_type_layouts.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft)

        #Number of Questions
        num_questions_layout = QHBoxLayout()

        num_questions_label = QLabel("Number of questions")
        num_questions_label.setFont(check_box_font)

        self.num_questions_input = QSpinBox()
        self.num_questions_input.setFixedSize(int(75 * self.widthScale), int(28 * self.widthScale))
        self.num_questions_input.setReadOnly(True)
        self.num_questions_input.setFont(check_box_font)
        self.num_questions_input.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.num_questions_input.setButtonSymbols(QAbstractSpinBox.ButtonSymbols.NoButtons)

        self.use_whole_set_cb = QCheckBox("Use entire set")
        self.use_whole_set_cb.setFont(check_box_font)
        self.use_whole_set_cb.setChecked(True)
        self.use_whole_set_cb.clicked.connect(self.checkGameSettings)

        num_questions_layout.addWidget(num_questions_label)
        num_questions_layout.addWidget(self.num_questions_input)
        num_questions_layout.addSpacing(int(50 * self.widthScale))
        num_questions_layout.addWidget(self.use_whole_set_cb)
        num_questions_layout.setAlignment(Qt.AlignmentFlag.AlignLeft)
        
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
        start_up_layout.addLayout(num_questions_layout)
        start_up_layout.addSpacing(int(25 * self.heightScale))
        start_up_layout.addLayout(start_game_layout)
        start_up_layout.addWidget(self.error_label)
        start_up_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        start_up_container.setLayout(start_up_layout)

        self.checkGameSettings()

        return start_up_container
    
    #Generate Layout Container where all questions will be stored
    def genGameLayout(self):
        main_game_container = QWidget()
        main_game_layout = QVBoxLayout()

        #Score Layout (Originally Hidden)
        self.score_container = QWidget()
        score_layout = QVBoxLayout()
        
        self.score_label = QLabel("Your Score:")
        score_font = QFont()
        score_font.setPointSize(20)
        score_font.setBold(True)
        self.score_label.setFont(score_font)

        score_layout.addWidget(self.score_label)
        score_layout.addSpacing(int(50 * self.heightScale))
        score_layout.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignHCenter)
        self.score_container.setLayout(score_layout)
        self.score_container.setHidden(True)

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

        #Submit Answers
        self.submit_answers_container = QWidget()
        submit_answers_layout = QHBoxLayout()
        
        submit_answers_button = QPushButton("Submit")
        submit_answers_button.setFixedSize(int(100 * self.widthScale), int(50 * self.heightScale))
        submit_answers_button.clicked.connect(self.checkAnswers)

        submit_answers_layout.addWidget(submit_answers_button)
        submit_answers_layout.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        self.submit_answers_container.setLayout(submit_answers_layout)

        #Replay or finish the game
        self.game_end_container = QWidget()

        game_end_layout = QHBoxLayout()

        replay_button = QPushButton("Replay")
        finish_game_button = QPushButton("Finish")

        replay_button.setFixedSize(int(100 * self.widthScale), int(50 * self.heightScale))
        finish_game_button.setFixedSize(int(100 * self.widthScale), int(50 * self.heightScale))

        replay_button.clicked.connect(self.replayGame)
        finish_game_button.clicked.connect(self.cancelGame)

        game_end_layout.addStretch(1)
        game_end_layout.addWidget(replay_button)
        game_end_layout.addSpacing(int(100 * self.widthScale))
        game_end_layout.addWidget(finish_game_button)
        game_end_layout.addStretch(1)

        self.game_end_container.setLayout(game_end_layout)
        self.game_end_container.setHidden(True)

        main_game_layout.addWidget(self.score_container)
        main_game_layout.addWidget(self.mc_sub_title_container)
        main_game_layout.addLayout(self.multiple_choice_questions_layout)
        main_game_layout.addWidget(self.ma_sub_title_container)
        main_game_layout.addLayout(self.matching_questions_layout)
        main_game_layout.addWidget(self.tf_sub_title_container)
        main_game_layout.addLayout(self.true_false_questions_layout)
        main_game_layout.addWidget(self.ta_sub_title_container)
        main_game_layout.addLayout(self.type_answer_questions_layout)
        main_game_layout.addSpacing(int(25 * self.heightScale))
        main_game_layout.addWidget(self.submit_answers_container)
        main_game_layout.addWidget(self.game_end_container)
        main_game_layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        main_game_container.setLayout(main_game_layout)
        return main_game_container
    
    #Add a multiple choice question
    def addMultipleChoiceQuestion(self):
        #Generate the layout and widgets
        main_mc_layout = QVBoxLayout()

        question_layout = QHBoxLayout()

        question_label = QLabel("Sample Question")
        question_font = QFont()
        question_font.setPointSize(14)
        question_label.setFont(question_font)
        question_label.setWordWrap(True)
        question_label.setAlignment(Qt.AlignmentFlag.AlignHCenter)

        question_layout.addWidget(question_label)
        question_layout.setAlignment(Qt.AlignmentFlag.AlignHCenter)

        radio_button_container = QWidget()
        radio_button_layout = QVBoxLayout()
        radio_buttons = []
        button_labels = []
        button_layouts = []
        for i in range(4):
            button_text_layout = QHBoxLayout()

            button_text_label = QLabel()
            button_text_label.setWordWrap(True)
            button_text_label.setFixedWidth(int(500 * self.widthScale))

            new_button = QRadioButton()
            new_button.setParent(radio_button_container)

            button_text_layout.addSpacing(int(300 * self.widthScale))
            button_text_layout.addWidget(new_button)
            button_text_layout.addWidget(button_text_label)
            button_text_layout.setAlignment(Qt.AlignmentFlag.AlignLeft)
            
            radio_button_layout.addLayout(button_text_layout)

            button_layouts.append(button_text_layout)
            button_labels.append(button_text_label)
            radio_buttons.append(new_button)

        radio_button_container.setLayout(radio_button_layout)

        main_mc_layout.addLayout(question_layout)
        main_mc_layout.addWidget(radio_button_container)
        main_mc_layout.addSpacing(int(25 * self.heightScale))
        main_mc_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        
        self.multiple_choice_questions_layout.addLayout(main_mc_layout)
        
        #Create Object for storage
        mc_question = MultipleChoiceQuestion(main_mc_layout, question_layout, question_label, radio_button_container, radio_button_layout, radio_buttons, button_labels, button_layouts)
        self.multiple_choice_questions.append(mc_question)

    #Add a matching question
    def addMatchingQuestion(self):
        matching_container = QVBoxLayout()
        main_matching_layout = QHBoxLayout()

        matching_input = QLineEdit()
        matching_input.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        matching_input.setFixedSize(int(50 * self.widthScale), int(25 * self.heightScale))
        matching_input.setAlignment(Qt.AlignmentFlag.AlignTop)
        
        question_font = QFont()
        question_font.setPointSize(14)

        matching_input_label = QLabel()
        matching_input_label.setWordWrap(True)
        matching_input_label.setFixedWidth(int(250 * self.widthScale))
        matching_input_label.setAlignment(Qt.AlignmentFlag.AlignLeft)
        matching_input_label.setFont(question_font)

        matching_answer_label = QLabel()
        matching_answer_label.setWordWrap(True)
        matching_answer_label.setFixedWidth(int(250 * self.widthScale))
        matching_answer_label.setAlignment(Qt.AlignmentFlag.AlignRight)
        matching_answer_label.setFont(question_font)

        reveal_answer_layout = QHBoxLayout()

        reveal_answer_label = QLabel("Sample Reveal")
        reveal_answer_label.setFont(question_font)
        reveal_answer_label.setHidden(True)

        reveal_answer_layout.addSpacing(int(100 * self.widthScale))
        reveal_answer_layout.addWidget(reveal_answer_label)
        reveal_answer_layout.setAlignment(Qt.AlignmentFlag.AlignLeft)

        main_matching_layout.addSpacing(int(100 * self.widthScale))
        main_matching_layout.addWidget(matching_input)
        main_matching_layout.addWidget(matching_input_label)
        main_matching_layout.addStretch(1)
        main_matching_layout.addWidget(matching_answer_label)
        main_matching_layout.addSpacing(int(100 * self.widthScale))
        main_matching_layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        matching_container.addLayout(main_matching_layout)
        matching_container.addLayout(reveal_answer_layout)
        matching_container.addSpacing(int(25 * self.heightScale))
        matching_container.setAlignment(Qt.AlignmentFlag.AlignLeft)
        
        self.matching_questions_layout.addLayout(matching_container)

        #Create and store object
        matching_obj = MatchingQuestion(matching_container, main_matching_layout, matching_input, matching_input_label, matching_answer_label, reveal_answer_layout, reveal_answer_label)
        self.matching_questions.append(matching_obj)

    #Add a true or false question
    def addTrueFalseQuestion(self):
        main_true_false_layout = QVBoxLayout()

        true_false_question_layout = QHBoxLayout()

        true_false_question_label = QLabel()
        true_false_question_font = QFont()
        true_false_question_font.setPointSize(14)
        true_false_question_label.setFont(true_false_question_font)
        true_false_question_label.setWordWrap(True)
        true_false_question_label.setFixedWidth(int(600 * self.heightScale))
        true_false_question_label.setAlignment(Qt.AlignmentFlag.AlignHCenter)

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
        main_true_false_layout.addSpacing(int(25 * self.heightScale))
        main_true_false_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        
        self.true_false_questions_layout.addLayout(main_true_false_layout)

        #Create and store object
        tf_object = TrueFalseQuestion(main_true_false_layout, true_false_question_layout, true_false_question_label, true_false_options_container, true_false_space_layout, true_false_options_layout, true_button, false_button)
        self.true_false_questions.append(tf_object)

    #Add a type answer question
    def addTypeAnswerQuestion(self):
        main_type_answer_layout = QVBoxLayout()

        main_type_answer_label_layout = QHBoxLayout()

        main_type_answer_label = QLabel()
        main_type_answer_font = QFont()
        main_type_answer_font.setPointSize(14)
        main_type_answer_label.setFont(main_type_answer_font)
        main_type_answer_label.setWordWrap(True)
        main_type_answer_label.setFixedWidth(int(600 * self.heightScale))
        main_type_answer_label.setAlignment(Qt.AlignmentFlag.AlignHCenter)

        main_type_answer_label_layout.addWidget(main_type_answer_label)
        main_type_answer_label_layout.setAlignment(Qt.AlignmentFlag.AlignHCenter)

        main_type_answer_input_layout = QHBoxLayout()

        main_type_answer_input = QLineEdit()
        main_type_answer_input.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        main_type_answer_input.setFixedWidth(int(600 * self.widthScale))

        main_type_answer_input_layout.addStretch(1)
        main_type_answer_input_layout.addWidget(main_type_answer_input)
        main_type_answer_input_layout.addStretch(1)

        answer_reveal_layout = QHBoxLayout()

        answer_reveal_label = QLabel("Sample Reveal")
        answer_reveal_label.setFont(main_type_answer_font)
        answer_reveal_label.setHidden(True)

        answer_reveal_layout.addWidget(answer_reveal_label)
        answer_reveal_layout.setAlignment(Qt.AlignmentFlag.AlignHCenter)

        main_type_answer_layout.addLayout(main_type_answer_label_layout)
        main_type_answer_layout.addLayout(main_type_answer_input_layout)
        main_type_answer_layout.addLayout(answer_reveal_layout)
        main_type_answer_layout.addSpacing(int(25 * self.heightScale))
        main_type_answer_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        
        self.type_answer_questions_layout.addLayout(main_type_answer_layout)

        #Create and store object
        type_obj = TypeAnswerQuestion(main_type_answer_layout, main_type_answer_label_layout, main_type_answer_label, main_type_answer_input_layout, main_type_answer_input, answer_reveal_layout, answer_reveal_label)
        self.type_answer_questions.append(type_obj)

    #Show/Hide the main container
    def setHidden(self, status):
        self.main_quiz_container.setHidden(status)



    #----------------------------------------------------------
    # Main Game Methods
    #----------------------------------------------------------
        
    #Start the quiz game
    def startGame(self):
        #Make sure number of questions is valid
        if self.num_questions_input.value() <= 4:
            self.message_signal.emit(['Error', 'Minimum of 5 questions required.'])
            return
        
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

        #If user opted to use the whole set, just shuffle. If they opted to select a certain amount of questions, then randomly select them
        if self.use_whole_set_cb.isChecked():
            set_content = self.shuffle(set_content)
        else:
            temp = []
            question_indexes = random.sample(range(len(set_content)), self.num_questions_input.value())
            for ind in question_indexes:
                temp.append(set_content[ind])
            
            set_content = temp

        #Figure out how many of each question type should be generated
        divisor = self.question_types.count(True)
        num_per_question_type = math.floor(len(set_content) / divisor)
        num_extra_questions = len(set_content) % divisor

        #Generate and populate all questions
        self.genAllQuestions(num_per_question_type, num_extra_questions)

        self.fillAllQuestions(set_content)

        for mc in self.multiple_choice_questions:
            self.all_answers.append(mc.getAnswer())

        for ma in self.matching_questions:
            self.all_answers.append(ma.getAnswer())
            self.matching_answers.append(ma.getAnswer())

        for tf in self.true_false_questions:
            self.all_answers.append(tf.getAnswer())

        for ta in self.type_answer_questions:
            self.all_answers.append(ta.getAnswer())

        self.fillAllAnswers()

    #Function for generating questions
    def genAllQuestions(self, baseline, extra):
        num_mc, num_ma, num_tf, num_ta = 0,0,0,0

        #Check multiple choice first since I chose a stupid order
        if self.question_types[0]:
            self.mc_sub_title_container.setHidden(False)
            num_mc = baseline
            if (self.question_types[1] and extra > 1) or (not(self.question_types[1]) and extra > 0): #Add extra question to mc if conditions are right
                num_mc += 1
                extra -= 1
        else:
            self.mc_sub_title_container.setHidden(True)
            
        if self.question_types[1]:
            self.ma_sub_title_container.setHidden(False)
            num_ma = baseline
            if extra > 0:
                num_ma += 1
                extra -= 1
        else:
            self.ma_sub_title_container.setHidden(True)

        if self.question_types[2]:
            self.tf_sub_title_container.setHidden(False)
            num_tf = baseline
            if extra:
                num_tf += 1
                extra -= 1
        else:
            self.tf_sub_title_container.setHidden(True)

        if self.question_types[3]:
            self.ta_sub_title_container.setHidden(False)
            num_ta = baseline
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

    #Fill all question labels
    def fillAllQuestions(self, set_data):
        #Fill all terms and definitions storage for true false questions
        for pair in set_data:
            contents = pair.split(':')
            self.all_terms.append(contents[0])
            self.all_defs.append(contents[1])

        #Fill multiple choice question labels
        for mc in range(len(self.multiple_choice_questions)):
            #Pull then delete data pair
            contents = set_data[0].split(':')
            set_data.pop(0)
            if self.gamemode < 2: #Definition is the question, at least initially 
                self.multiple_choice_questions[mc].setQuestionAndAnswer(contents[1], contents[0], self.gamemode)
            else: #Definition is the term
                self.multiple_choice_questions[mc].setQuestionAndAnswer(contents[0], contents[1], self.gamemode)

        #Fill matching question labels
        for ma in range(len(self.matching_questions)):
            #Pull then delete data pair
            contents = set_data[0].split(':')
            set_data.pop(0)
            if self.gamemode < 2: #Definition is the question, at least initially 
                self.matching_questions[ma].setQuestionAndAnswer(contents[1], contents[0], self.gamemode)
            else: #Definition is the term
                self.matching_questions[ma].setQuestionAndAnswer(contents[0], contents[1], self.gamemode)

        #Set True/False Questions and Answers(Label is set during answer functions)
        for tf in range(len(self.true_false_questions)):
            #Pull then delete data pair
            contents = set_data[0].split(':')
            set_data.pop(0)
            if self.gamemode < 2: #Definition is the question, at least initially 
                self.true_false_questions[tf].setQuestionAndAnswer(contents[1], contents[0], self.gamemode)
            else: #Definition is the term
                self.true_false_questions[tf].setQuestionAndAnswer(contents[0], contents[1], self.gamemode)
        
        #Fill out type answer labels        
        for ta in range(len(self.type_answer_questions)):
            #Pull then delete data pair
            contents = set_data[0].split(':')
            set_data.pop(0)
            if self.gamemode < 2: #Definition is the question, at least initially 
                self.type_answer_questions[ta].setQuestionAndAnswer(contents[1], contents[0], self.gamemode)
            else: #Definition is the term
                self.type_answer_questions[ta].setQuestionAndAnswer(contents[0], contents[1], self.gamemode)
            
    #Fill all answers of each question type
    def fillAllAnswers(self):
        #Multiple Choice Questions
        for mc in self.multiple_choice_questions:
            mc.setAnswerOptions(self.all_answers)

        #Matching
        self.matching_answers = self.shuffle(self.matching_answers)
        temp_list = []
        for val in self.matching_answers:
            temp_list.append(val)
        
        for ma in range(len(self.matching_questions)):
            del_ind = self.matching_questions[ma].setAnswerLabel(ma, temp_list)
            del temp_list[del_ind]

        #True False
        for tf in self.true_false_questions:
            tf.setQuestionLabel(self.all_terms, self.all_defs, self.gamemode)

    #Populate Set Dropdown
    def populateSetDD(self):
        while self.select_set_dd.count() > 0:
            self.select_set_dd.removeItem(0)
        
        set_titles = self.set_data.getAllSetTitles()

        del set_titles[0] #Remove placeholder set
        self.select_set_dd.addItems(set_titles)

    #Verify that the question type settings are valid
    def checkGameSettings(self):
        #Get data of set current selected in the drop down
        current_set_index = self.select_set_dd.currentIndex()
        current_set_title = self.set_data.getSetTitle(current_set_index)
        current_set_data = self.set_data.getSetContent(current_set_title)

        #Set the number of questions in the box when changing dropdown menu (This part does not effect the rest, so it is done first)
        self.num_questions_input.setMaximum(len(current_set_data))
        if self.use_whole_set_cb.isChecked():
            self.num_questions_input.setReadOnly(True)
            self.num_questions_input.setValue(len(current_set_data))
        else:
            self.num_questions_input.setReadOnly(False)

        #Make sure at least one checkbox is selected
        if (not self.multiple_choice_cb.isChecked()) and (not self.matching_cb.isChecked()) and (not self.true_false_cb.isChecked()) and (not self.type_answers_cb.isChecked()):
            self.start_game_button.setEnabled(False)
        else:
            self.start_game_button.setEnabled(True)

        #Make sure set is long enough to run a game
        if len(current_set_data) <= 4:
            self.start_game_button.setEnabled(False)
            self.error_label.setHidden(False)
        else:
            self.start_game_button.setEnabled(True)
            self.error_label.setHidden(True) 
    
    #Check the answers (Slot function for submit button)
    def checkAnswers(self):
        #Intialize trackers for storing the amount correct and incorrect answers
        correct_counter = 0
        incorrect_counter = 0

        #All answers have an input. Now check answers
        allAnswered = self.questionsAnswered()
        if not allAnswered:
            self.message_signal.emit(['Error', 'At least 1 question is unanswered.\nMake sure all questions are answered before submitting.'])
            return
        
        #Check the correctness
        for mc in self.multiple_choice_questions:
            isCorrect = mc.checkAnswer()
            if isCorrect:
                correct_counter += 1
            else:
                incorrect_counter += 1
                
        for ma in self.matching_questions:
            selected_ind = ma.findLetterIndex()
            if not selected_ind and selected_ind != 0:
                incorrect_counter += 1
                continue

            if selected_ind >= len(self.matching_questions):
                ma.showCorrectAnswer()
                incorrect_counter += 1
                continue

            isCorrect = ma.checkAnswer(self.matching_questions[selected_ind].getCorrespondingAnswer())
            if isCorrect:
                correct_counter += 1
            else:
                incorrect_counter += 1
        
        for tf in self.true_false_questions:
            isCorrect = tf.checkAnswer()
            if isCorrect:
                correct_counter += 1
            else:
                incorrect_counter += 1
        
        for ta in self.type_answer_questions:
            isCorrect = ta.checkAnswer()
            if isCorrect:
                correct_counter += 1
            else:
                incorrect_counter += 1

        #Update and display score
        score = int((correct_counter / (correct_counter + incorrect_counter)) * 100)
        self.score_label.setText("Your Score: {}%".format(score))
        self.score_container.setHidden(False)

        #Change Options for next options
        self.submit_answers_container.setHidden(True)
        self.game_end_container.setHidden(False)

        #Set scroll area to top
        self.main_game_scroll_area.verticalScrollBar().setValue(0)
        
    #Check if any questions are missing an answer
    def questionsAnswered(self):
        #Ensure all questions are answered
        for mc in self.multiple_choice_questions:
            was_answered = mc.isAnswered()
            if not was_answered:
                return False
            
        for ma in self.matching_questions:
            was_answered = ma.isAnswered()
            if not was_answered:
                return False
            
        for tf in self.true_false_questions:
            was_answered = tf.isAnswered()
            if not was_answered:
                return False
            
        for ta in self.type_answer_questions:
            was_answered = ta.isAnswered()
            if not was_answered:
                return False
            
        return True

    #Cancel Game
    def cancelGame(self):
        self.resetGame()

        self.main_game_scroll_area.setHidden(True)
        self.exit_game_button.setHidden(True)
        self.start_up_container.setHidden(False)

    #Replay Game
    def replayGame(self):
        self.resetGame()
        self.startGame()

    #Reset Game
    def resetGame(self):
        self.clearQuestions()

        self.multiple_choice_questions = []
        self.matching_questions = []
        self.true_false_questions = []
        self.type_answer_questions = []
    
        self.question_types = []
        self.gamemode = 0
        self.all_answers = []
        self.matching_answers = []

        self.all_terms = []
        self.all_defs = []

        self.score_container.setHidden(True)
        self.game_end_container.setHidden(True)
        self.submit_answers_container.setHidden(False)
        
    #Clear all questions from the scroll area
    def clearQuestions(self):
        for mc in self.multiple_choice_questions:
            mc.deleteQuestion() 

        for ma in self.matching_questions:
            ma.deleteQuestion()

        for tf in self.true_false_questions:
            tf.deleteQuestion()

        for ta in self.type_answer_questions:
            ta.deleteQuestion()

    #Shuffle a list
    def shuffle(self, arr):
        temp = []
        while len(arr) > 0:
            randomInd = random.randint(0, len(arr) - 1)
            temp.append(arr[randomInd])
            del arr[randomInd]
        
        return temp
        
        