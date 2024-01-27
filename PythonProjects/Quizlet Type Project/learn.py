#This file will be used for the match game.

#Imports
import random
from decorators import log_start_and_stop
from Sets import Sets

from PyQt6.QtWidgets import ( 
    QHBoxLayout, QVBoxLayout, QWidget,
    QPushButton, QLineEdit, QSpacerItem,
    QLabel, QComboBox, QSizePolicy,
    QRadioButton
)
from PyQt6.QtCore import QObject, Qt, pyqtSignal
from PyQt6.QtGui import QGuiApplication, QFont

#Question Class
class Question:
    #Constructor
    def __init__(self):
        self.question = None
        self.answer = None
        self.stage = 0 #0 for multiple choice, 1 for typing out answer
        self.q_type = 0 #0 For both question types, 1 for multiple choice, 2 for typing out answer

    #Getters
    def getQuestion(self):
        return self.question
    
    def getAnswer(self):
        return self.answer
    
    def getStage(self):
        return self.stage
    
    #Setters
    def setQuestion(self, q):
        self.question = q

    def setAnswer(self, a):
        self.answer = a

    def setQuestionType(self, t):
        self.q_type = t

    def goNextStage(self): #Returns False if the question is not complete, returns True if it is
        if self.q_type > 0:
            return True
        
        self.stage += 1 
        if self.stage > 1:
            return True
        return False

    #If the user chose the random gamemode, the question and answer should be randomized for each stage, not just the learn run
    def randomizeQandA(self):
        doSwitch = random.randint(0, 1)
        if doSwitch == 0:
            temp = self.question
            self.question = self.answer
            self.answer = temp
        
    
#Match Class
class Learn(QObject):
    #Signals
    messageSignal = pyqtSignal(list)

    #Constructor
    def __init__(self):
        #Call Parent Constructor method
        super().__init__()

        #Intialize Learn Variables
        self.questions = []
        self.all_answers = [] #Copy of question objects should be stored should multiple choice be selected
        self.gamemode = 0
        self.question_type = 0 #0: All question types: 1: Multiple Choice Only 2: Type answers only
        self.mixedFlag = 0

        #Access to Set data
        self.setData = Sets()

    #-------------------------------------
    # GUI Widget Methods
    #-------------------------------------
    
    #Generate The Match Container Layout
    def genLearnLayout(self):
        #Get Scales
        screen_resolution = QGuiApplication.primaryScreen().availableGeometry()
        width, height = screen_resolution.width(), screen_resolution.height()
        self.widthScale = width / 1920
        self.heightScale = height / 1032

        self.learn_container = QWidget()
        self.main_learn_layout = QVBoxLayout()

        #Match home screen
        learn_title_label = QLabel("Learn!")
        learn_title_font = QFont()
        learn_title_font.setPointSize(24)
        learn_title_font.setBold(True)
        learn_title_label.setFont(learn_title_font)
        learn_title_label.setAlignment(Qt.AlignmentFlag.AlignHCenter)

        self.start_learn_layout = QVBoxLayout()
        self.start_learn_container = QWidget()

        #Create the options for selecting a set to study
        options_title_layout = QHBoxLayout()

        options_title_label = QLabel("Game Options")
        options_title_font = QFont()
        options_title_font.setPointSize(18)
        options_title_font.setBold(True)
        options_title_label.setFont(options_title_font)

        options_title_layout.addWidget(options_title_label)
        options_title_layout.setAlignment(Qt.AlignmentFlag.AlignHCenter)

        #Select Set
        select_set_layout = QHBoxLayout()

        select_set_label = QLabel("Select Set:")
        game_options_font = QFont()
        game_options_font.setPointSize(14)
        select_set_label.setFont(game_options_font)

        self.selectSetDD = QComboBox()
        self.selectSetDD.setFixedSize(int(200 * self.widthScale), int(30 * self.heightScale))
        self.populateSetDD()

        select_set_layout.addWidget(select_set_label)
        select_set_layout.addSpacing(int(10 * self.widthScale))
        select_set_layout.addWidget(self.selectSetDD)
        select_set_layout.setAlignment(Qt.AlignmentFlag.AlignLeft)

        #Game Order
        game_order_layout = QHBoxLayout()

        game_order_label = QLabel("Order:")
        game_order_label.setFont(game_options_font)

        self.select_gamemode_dd = QComboBox()
        self.select_gamemode_dd.setFixedHeight(int(30 * self.heightScale))
        gamemode_options = ['Given Definition, Enter Term', 'Given Term, Enter Definition', 'Mixed']
        self.select_gamemode_dd.addItems(gamemode_options)

        game_order_layout.addWidget(game_order_label)
        game_order_layout.addSpacing(int(10 * self.widthScale))
        game_order_layout.addWidget(self.select_gamemode_dd)
        game_order_layout.setAlignment(Qt.AlignmentFlag.AlignLeft)

        #Question Types
        question_type_layout = QHBoxLayout()

        question_type_label = QLabel("Question Types:")
        question_type_label.setFont(game_options_font)

        self.select_question_type_dd = QComboBox()
        self.select_question_type_dd.setFixedHeight(int(30 * self.heightScale))
        question_type_options = ['All question types', 'Multiple choice only', 'Type answers only']
        self.select_question_type_dd.addItems(question_type_options)

        question_type_layout.addWidget(question_type_label)
        question_type_layout.addSpacing(int(10 * self.widthScale))
        question_type_layout.addWidget(self.select_question_type_dd)
        question_type_layout.setAlignment(Qt.AlignmentFlag.AlignLeft)
        
        #Start Game
        start_game_layout = QHBoxLayout()

        self.start_game_button = QPushButton('Start')
        self.start_game_button.setFixedSize(int(100 * self.widthScale), int(50 * self.heightScale))
        self.start_game_button.clicked.connect(self.startGame)
        
        start_game_layout.addWidget(self.start_game_button)
        start_game_layout.setAlignment(Qt.AlignmentFlag.AlignHCenter)

        self.start_learn_layout.addLayout(options_title_layout)
        self.start_learn_layout.addSpacing(int(25 * self.heightScale))
        self.start_learn_layout.addLayout(select_set_layout)
        self.start_learn_layout.addSpacing(int(10 * self.heightScale))
        self.start_learn_layout.addLayout(game_order_layout)
        self.start_learn_layout.addSpacing(int(10 * self.heightScale))
        self.start_learn_layout.addLayout(question_type_layout)
        self.start_learn_layout.addSpacing(int(40 * self.heightScale))
        self.start_learn_layout.addLayout(start_game_layout)
        self.start_learn_layout.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        self.start_learn_container.setLayout(self.start_learn_layout)
        
        #Match Multiple Choice Layout
        self.genMultipleChoiceLayout()

        #Match Write Answer Layout
        self.main_type_answer_layout = QVBoxLayout()
        self.main_type_answer_container = QWidget()
        
        question_text_font = QFont()
        question_text_font.setPointSize(14)

        self.question_tracker_container = QWidget()
        self.question_tracker_layout = QHBoxLayout()
        self.question_tracker_label = QLabel('Questions fully completed: 0/0')
        self.question_tracker_label.setFont(question_text_font)
        
        self.question_tracker_layout.addWidget(self.question_tracker_label)
        self.question_tracker_layout.addSpacerItem(QSpacerItem(int(300 * self.widthScale), 0, QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Minimum))
        self.question_tracker_layout.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.question_tracker_container.setLayout(self.question_tracker_layout)
        self.question_tracker_container.setHidden(True)
        
        self.type_answer_question_layout = QHBoxLayout()
        self.type_answer_question_label = QLabel('Sample Question')
        self.type_answer_question_label.setWordWrap(True)
        self.type_answer_question_label.setFont(question_text_font)
        
        self.type_answer_question_layout.addWidget(self.type_answer_question_label)
        self.type_answer_question_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        self.type_answer_layout = QHBoxLayout() 
        self.type_answer_input = QLineEdit()
        self.submit_type_answer_btn = QPushButton('Check')
        
        self.type_answer_input.returnPressed.connect(self.checkTypeAnswer)
        self.submit_type_answer_btn.clicked.connect(self.checkTypeAnswer)
        
        type_answer_font = QFont()
        type_answer_font.setPointSize(16)
        self.type_answer_input.setFont(type_answer_font)
        self.type_answer_input.setFixedSize(int(500 * self.widthScale), int(40 * self.heightScale))
        self.type_answer_input.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Preferred)

        self.submit_type_answer_btn.setFixedSize(int(100 * self.widthScale), int(40 * self.heightScale))
        self.submit_type_answer_btn.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        
        self.type_answer_layout.addWidget(self.type_answer_input)
        self.type_answer_layout.addWidget(self.submit_type_answer_btn)
        self.type_answer_layout.setAlignment(Qt.AlignmentFlag.AlignHCenter)

        #Combine Main Game Layout
        self.main_type_answer_layout.addLayout(self.type_answer_question_layout)
        self.main_type_answer_layout.addSpacerItem(QSpacerItem(0, int(25 * self.heightScale), QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed))
        self.main_type_answer_layout.addLayout(self.type_answer_layout)
        self.main_type_answer_container.setLayout(self.main_type_answer_layout)
        self.main_type_answer_container.setHidden(True)

        #Layout for correct answer
        self.answered_correct_layout = QVBoxLayout()
        self.answered_correct_container = QWidget()
        
        answered_correct_label = QLabel('Correct!')
        answered_correct_font = QFont()
        answered_correct_font.setPointSize(24)
        answered_correct_label.setFont(answered_correct_font)
        answered_correct_label.setAlignment(Qt.AlignmentFlag.AlignHCenter)

        self.next_question_btn = QPushButton('Next')
        self.next_question_btn.setFixedSize(int(100 * self.widthScale), int(40 * self.heightScale))
        self.next_question_btn.clicked.connect(self.startNextQuestion)

        self.answered_correct_layout.addWidget(answered_correct_label)
        self.answered_correct_layout.addSpacerItem(QSpacerItem(0, int(25 * self.heightScale), QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed))
        self.answered_correct_layout.addWidget(self.next_question_btn)
        self.answered_correct_layout.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        self.answered_correct_container.setLayout(self.answered_correct_layout)
        self.answered_correct_container.setHidden(True)
        
        #Layout for incorrect answer
        self.answered_incorrect_layout = QWidget()
        self.answered_incorrect_container = QVBoxLayout()

        answered_incorrect_label = QLabel('Incorrect')
        answered_incorrect_label.setFont(answered_correct_font)

        self.answered_incorrect_display_label = QLabel('The correct answer was: ')
        self.answered_incorrect_display_label.setFont(type_answer_font)

        self.user_answer_label = QLabel('Your answer was: ')
        self.user_answer_label.setFont(type_answer_font)

        self.incorrect_answer_continue_option_layout = QHBoxLayout()
        self.override_incorrect_answer_btn = QPushButton('Override, I was right.')
        self.continueWithWrongAnswerBtn = QPushButton('Continue')

        self.override_incorrect_answer_btn.clicked.connect(self.overrideWrongAnswer)
        self.continueWithWrongAnswerBtn.clicked.connect(self.continueWithWrongAnswer)

        self.incorrect_answer_continue_option_layout.addWidget(self.override_incorrect_answer_btn)
        self.incorrect_answer_continue_option_layout.addWidget(self.continueWithWrongAnswerBtn)
        self.incorrect_answer_continue_option_layout.setAlignment(Qt.AlignmentFlag.AlignHCenter)

        self.answered_incorrect_container.addWidget(answered_incorrect_label)
        self.answered_incorrect_container.addWidget(self.answered_incorrect_display_label)
        self.answered_incorrect_container.addWidget(self.user_answer_label)
        self.answered_incorrect_container.addLayout(self.incorrect_answer_continue_option_layout)
        self.answered_incorrect_container.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        self.answered_incorrect_layout.setLayout(self.answered_incorrect_container)
        self.answered_incorrect_layout.setHidden(True)

        #Match completed screen
        self.game_completed_container = QWidget()
        self.game_completed_layout = QVBoxLayout()
        
        game_label_layout = QHBoxLayout()

        game_completed_label = QLabel('Good Job!')
        game_completed_label.setFont(answered_correct_font)

        game_label_layout.addWidget(game_completed_label)
        game_label_layout.setAlignment(Qt.AlignmentFlag.AlignHCenter)

        self.game_score_label = QLabel("Your score was: ")
        self.game_score_label.setFont(answered_correct_font)

        self.game_completed_btn_layout = QHBoxLayout()

        self.replay_match_btn = QPushButton('Replay set')
        self.finish_match_btn = QPushButton('Finish')

        self.replay_match_btn.clicked.connect(self.replayGame)
        self.finish_match_btn.clicked.connect(self.setGameHomeScreen)

        self.game_completed_btn_layout.addWidget(self.replay_match_btn)
        self.game_completed_btn_layout.addWidget(self.finish_match_btn)

        self.game_completed_layout.addLayout(game_label_layout)
        self.game_completed_layout.addSpacing(int(20 * self.heightScale))
        self.game_completed_layout.addWidget(self.game_score_label)
        self.game_completed_layout.addLayout(self.game_completed_btn_layout)
        self.game_completed_layout.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        self.game_completed_container.setLayout(self.game_completed_layout)
        self.game_completed_container.setHidden(True)
        
        #Cancel Match Game Option
        self.cancel_game_container = QWidget()
        self.cancel_game_layout = QHBoxLayout()
        
        self.cancel_game_btn = QPushButton('Exit')
        self.cancel_game_btn.setFixedSize(int(100 * self.widthScale), int(50 * self.heightScale))
        self.cancel_game_btn.clicked.connect(self.cancelGame)
        
        self.cancel_game_layout.addSpacing(int(300 * self.widthScale))
        self.cancel_game_layout.addWidget(self.cancel_game_btn)
        self.cancel_game_layout.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.cancel_game_container.setLayout(self.cancel_game_layout)
        self.cancel_game_container.setHidden(True)

        #Container for all match layouts
        self.main_learn_layout.addSpacerItem(QSpacerItem(0, 0, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum))
        self.main_learn_layout.addWidget(learn_title_label)
        self.main_learn_layout.addSpacing(int(50 * self.heightScale))
        self.main_learn_layout.addWidget(self.question_tracker_container)
        self.main_learn_layout.addWidget(self.start_learn_container)
        self.main_learn_layout.addWidget(self.main_type_answer_container)
        self.main_learn_layout.addWidget(self.mult_choice_main_container)
        self.main_learn_layout.addWidget(self.answered_correct_container)
        self.main_learn_layout.addWidget(self.answered_incorrect_layout)
        self.main_learn_layout.addWidget(self.game_completed_container)
        self.main_learn_layout.addSpacerItem(QSpacerItem(0, int(40 * self.heightScale), QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed))
        self.main_learn_layout.addWidget(self.cancel_game_container)
        self.main_learn_layout.addSpacerItem(QSpacerItem(0, 0, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum))
        self.main_learn_layout.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignHCenter)
        self.learn_container.setLayout(self.main_learn_layout)
        self.learn_container.setHidden(True)

    #Create the multiple choice layout
    def genMultipleChoiceLayout(self):
        self.mult_choice_main_container = QWidget()
        mult_choice_main_layout = QVBoxLayout()

        mult_choice_question_layout = QHBoxLayout()

        self.mult_choice_question_label = QLabel('Sample Question')
        mult_choice_question_font = QFont()
        mult_choice_question_font.setPointSize(14)
        mult_choice_question_font.setBold(True)
        self.mult_choice_question_label.setFont(mult_choice_question_font)
        self.mult_choice_question_label.setWordWrap(True)
        self.mult_choice_question_label.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        self.mult_choice_question_label.setFixedWidth(int(500 * self.widthScale))

        mult_choice_question_layout.addWidget(self.mult_choice_question_label)
        mult_choice_question_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        mult_choice_answers_wrapper = QHBoxLayout()
        mult_choice_answers_layout = QVBoxLayout()
        
        self.mult_choice_answers = []
        self.mult_choice_labels = []
        for i in range(4):
            answer_layout = QHBoxLayout()

            answer_label = QLabel()
            answer_label.setWordWrap(True)

            new_button = QRadioButton()

            answer_layout.addWidget(new_button)
            answer_layout.addWidget(answer_label)
            answer_layout.setAlignment(Qt.AlignmentFlag.AlignLeft)

            mult_choice_answers_layout.addLayout(answer_layout)

            self.mult_choice_answers.append(new_button)
            self.mult_choice_labels.append(answer_label)
            

        mult_choice_answers_layout.setAlignment(Qt.AlignmentFlag.AlignLeft)

        mult_choice_answers_wrapper.addSpacing(int(300 * self.widthScale))
        mult_choice_answers_wrapper.addLayout(mult_choice_answers_layout)

        mult_choice_check_layout = QHBoxLayout()
        
        mult_choice_check_button = QPushButton("Check Answer")
        mult_choice_check_button.setFixedSize(int(125 * self.widthScale), int(50 * self.heightScale))
        mult_choice_check_button.clicked.connect(self.checkMultChoiceAnswer)

        mult_choice_check_layout.addWidget(mult_choice_check_button)
        mult_choice_check_layout.addSpacing(int(300 * self.widthScale))
        mult_choice_check_layout.setAlignment(Qt.AlignmentFlag.AlignRight)

        mult_choice_main_layout.addLayout(mult_choice_question_layout)
        mult_choice_main_layout.addSpacing(int(15 * self.widthScale))
        mult_choice_main_layout.addLayout(mult_choice_answers_wrapper)
        mult_choice_main_layout.addLayout(mult_choice_check_layout)
        self.mult_choice_main_container.setLayout(mult_choice_main_layout)
        self.mult_choice_main_container.setHidden(True)

    #Get the layout container
    def getLearnContainer(self):
        return self.learn_container
    
    #Show/Hide the Layout
    def setHidden(self, status):
        self.learn_container.setHidden(status)

    #Populate the select set dropdown menu in the match tab
    def populateSetDD(self):
        #Remove all old sets in case of update
        while self.selectSetDD.count() > 0:
            self.selectSetDD.removeItem(0)
        
        titles = self.setData.getAllSetTitles()

        for i in range(len(titles)):
            if i > 0: #Ensure hidden set is not added
                self.selectSetDD.addItem(titles[i])
    
    #-----------------------------------------
    # Main Game Methods
    #-----------------------------------------
    
    #Construct the main storage of the match game
    def addQuestion(self, question):
        question_content = question.split(':')
        term, definition = question_content[0], question_content[1]
        q = Question()

        #Given definition, enter term
        if self.gamemode == 0:
            q.setQuestion(definition)
            q.setAnswer(term)
        #Given term, enter definition
        else:
            q.setQuestion(term)
            q.setAnswer(definition)

        #If the user selected random, randomize which is question and which is answer
        if self.gamemode == 2:
            q.randomizeQandA()
        
        q.setQuestionType(self.question_type)

        self.questions.append(q)
    
    #Start the match game
    @log_start_and_stop
    def startGame(self, *args, **kwargs):
        #Pull match parameters
        learn_set_name = self.selectSetDD.currentText()
        gamemode = self.select_gamemode_dd.currentIndex()
        question_type = self.select_question_type_dd.currentIndex()
        
        #Get Set Data using set name
        learn_set_data = self.setData.getSetContent(learn_set_name)

        #Ensure set is still available
        if not learn_set_data:
            self.messageSignal.emit(['Error', "The program couldn't find the set selected."])
            return 

        #Set the match gamemode from input
        self.gamemode = gamemode
        self.question_type = question_type
        
        for item in learn_set_data:
            self.addQuestion(item)             
        
        if question_type < 2:
            #First check if the set length allows multiple choice
            if len(self.questions) < 4:
                self.resetGame()
                self.messageSignal.emit(['Error', 'Your set {} does not have enough pairs for multiple choice questions.\n(At least 4 are needed)'.format(learn_set_name)])
                return
            
            #Store answers for multiple choice options
            for q in self.questions:
                self.all_answers.append(q.getAnswer())     

            #Ensure all radio buttons are not checked
            for btn in self.mult_choice_answers:
                btn.setCheckable(False)
                btn.setCheckable(True)      
        
        #Shuffle the pairs
        self.shuffle()
        
        #Set match layout
        self.start_learn_container.setHidden(True)
        self.question_tracker_container.setHidden(False)

        if self.question_type == 2:
            self.main_type_answer_container.setHidden(False)
        else:
            self.mult_choice_main_container.setHidden(False)
        
        self.cancel_game_container.setHidden(False)
        
        #Initialize progress label info
        self.lenFullSet = len(self.questions)
        self.correctCounter = 0
        self.incorrect_counter = 0

        #Start game
        self.startNextQuestion()
    
    #Give user the next match question
    def startNextQuestion(self):
        #Show correct layout while hiding post-answer layouts
        self.answered_correct_container.setHidden(True)
        self.answered_incorrect_layout.setHidden(True)

        #Check current question stage
        current_question_stage = self.questions[0].getStage()
        if current_question_stage == 0 and self.question_type < 2:
            self.mult_choice_main_container.setHidden(False)
        else:
            self.main_type_answer_container.setHidden(False)

        #Set the progress label text
        self.question_tracker_label.setText('Questions fully completed: {}/{}'.format(self.correctCounter, self.lenFullSet))

        #Pull question text
        self.currentQuestion = self.questions[0]
        
        #Reset Question Height
        self.mult_choice_question_label.setFixedHeight(int(30 * self.heightScale))
        self.type_answer_question_label.setFixedHeight(int(30 * self.heightScale))

        self.populateQuestionScreen()
    
    #Populate the question screen. Should be used for both typed answers and multiple choice
    def populateQuestionScreen(self):
        #Question type is already determined in the prior method, so we only have to check the status of the layout containers
        if self.mult_choice_main_container.isHidden(): #Type answer
            self.type_answer_question_label.setText(self.currentQuestion.getQuestion())
            self.type_answer_question_label.setFixedHeight(self.type_answer_question_label.sizeHint().height())
        else: # Multiple Choice
            self.correct_index = random.randint(0, 3) #Index of which radio button will contain the correct answer

            #Set question label to the current questions text
            self.mult_choice_question_label.setText(self.currentQuestion.getQuestion())
            self.mult_choice_question_label.setFixedHeight(self.mult_choice_question_label.sizeHint().height())
            
            #Get random incorrect answers
            correct_answer_ind = self.all_answers.index(self.currentQuestion.getAnswer())

            answers = []
            answer_indexes = []
            while not answer_indexes or correct_answer_ind in answer_indexes:
                answer_indexes = random.sample(range(len(self.all_answers)), 3)
            
            for answer in answer_indexes:
                answers.append(self.all_answers[answer])
            
            #Populate radio buttons text
            for i in range(len(self.mult_choice_answers)):
                if i == self.correct_index:
                    self.mult_choice_labels[i].setText(self.currentQuestion.getAnswer())
                else:
                    self.mult_choice_labels[i].setText(answers[0])
                    answers.pop(0)

                self.mult_choice_labels[i].setFixedHeight(int(30 * self.heightScale)) #Reset Height if larger before
                self.mult_choice_labels[i].setFixedHeight(self.mult_choice_labels[i].sizeHint().height())

    #Check the selected multiple choice answer
    def checkMultChoiceAnswer(self):
        #First check if the user selected anything before going further
        flag = False
        for btn in self.mult_choice_answers:
            if btn.isChecked():
                flag = True
        
        if not flag:
            return
        
        #Check for index of selected answer, and compare to the correct index
        for i in range(len(self.mult_choice_answers)):
            if self.mult_choice_answers[i].isChecked():
                if i == self.correct_index:
                    self.answeredCorrect()
                    
                    if self.correctCounter >= self.lenFullSet:
                        self.matchComlpeted()
                        return

                    self.mult_choice_main_container.setHidden(True)
                    self.answered_correct_container.setHidden(False)
                else:
                    #Show an incorrect answer screen with override button hidden.
                    self.mult_choice_main_container.setHidden(True) 
                    self.override_incorrect_answer_btn.setHidden(True)
                    self.answered_incorrect_layout.setHidden(False)

                    self.answered_incorrect_display_label.setText('The correct answer was: {}'.format(self.currentQuestion.getAnswer()))
                    self.user_answer_label.setText('Your answer was: {}'.format(self.mult_choice_answers[i].text()))

            #Reset checked status of radio button
            self.mult_choice_answers[i].setCheckable(False)
            self.mult_choice_answers[i].setCheckable(True)
                    
    #Check user inputted answer
    def checkTypeAnswer(self):
        #Check is the user entered anything
        if not self.type_answer_input.text():
            return
        
        #Pull answer then wipe input
        userAnswer = self.type_answer_input.text()
        self.type_answer_input.setText('')
        isCorrect = (userAnswer.lower() == self.currentQuestion.getAnswer().lower())

        #Check answer
        if isCorrect:
            self.answeredCorrect()

            #Check if answer was the last question
            if self.correctCounter >= self.lenFullSet:
                self.matchComlpeted()
                return
             
            #Answer was correct, show correct layout, with button linked to start the next question
            self.main_type_answer_container.setHidden(True)
            self.answered_correct_container.setHidden(False)
        else:
            #Answer was incorrect, show incorrect answer layout, with a manual override, or continue button.
            self.main_type_answer_container.setHidden(True)
            self.override_incorrect_answer_btn.setHidden(False)
            self.answered_incorrect_layout.setHidden(False)

            #Show correct answer
            self.answered_incorrect_display_label.setText('The correct answer was: {}'.format(self.currentQuestion.getAnswer()))
            self.user_answer_label.setText('Your answer was: {}'.format(userAnswer))

    #Override incorrect answer
    def overrideWrongAnswer(self):
        #Act as if answer was correct
        self.answeredCorrect()

        #Check if answer was the last question
        if self.correctCounter >= self.lenFullSet:
            self.matchComlpeted()
            return
        
        #Continue with the game
        self.startNextQuestion()

    #Continue with wrong answer
    def continueWithWrongAnswer(self):
        self.incorrect_counter += 1
        self.reshuffleQuestion()
        self.startNextQuestion()

    #Show finished match screen
    @log_start_and_stop
    def matchComlpeted(self):
        #Calculate and update score
        score = int((self.correctCounter / (self.correctCounter + self.incorrect_counter)) * 100)
        self.game_score_label.setText("Your score was: {}%".format(score))

        #Reset match object
        self.resetGame()

        #Show the match complete screen
        self.answered_correct_container.setHidden(True)
        self.answered_incorrect_layout.setHidden(True)
        self.mult_choice_main_container.setHidden(True)
        self.main_type_answer_container.setHidden(True)
        self.cancel_game_container.setHidden(True)
        self.question_tracker_container.setHidden(True)
        self.game_completed_container.setHidden(False)      

    #Replay set button   
    def replayGame(self):
        self.game_completed_container.setHidden(True)
        self.startGame()

    #Reset match tab
    def setGameHomeScreen(self):
        self.game_completed_container.setHidden(True)
        self.start_learn_container.setHidden(False)

    #Cancel match mid-game
    def cancelGame(self):
        self.resetGame()
        
        self.answered_correct_container.setHidden(True)
        self.answered_incorrect_layout.setHidden(True)
        self.mult_choice_main_container.setHidden(True)
        self.main_type_answer_container.setHidden(True)
        self.question_tracker_container.setHidden(True)
        self.cancel_game_container.setHidden(True)
        self.start_learn_container.setHidden(False)  
            
    #Randomize the set
    @log_start_and_stop
    def shuffle(self):
        temp = []
        while len(self.questions) > 0:
            randomInd = random.randint(0, len(self.questions) - 1)
            temp.append(self.questions[randomInd])
            del self.questions[randomInd]
        
        self.questions = temp
        
    #Function for if user answered correctly
    @log_start_and_stop
    def answeredCorrect(self):
        is_complete = self.questions[0].goNextStage()
        if is_complete: 
            self.correctCounter += 1
            self.questions.pop(0)
        else:
            if self.gamemode == 2:
                self.questions[0].randomizeQandA()
            self.reshuffleQuestion()
        
    #Function for if the user answered incorrectly
    @log_start_and_stop
    def reshuffleQuestion(self):
        item = self.questions.pop(0)
        if len(self.questions) >= 1:
            newIndex = random.randint(1, len(self.questions))
            self.questions.insert(newIndex, item)
        else:
            self.questions.append(item)

    #Game is completed, reset the match obj
    def resetGame(self):
        self.questions = []
        self.all_answers = []
        self.question_type = 0
        self.gamemode = 0
        self.mixedFlag = 0
        