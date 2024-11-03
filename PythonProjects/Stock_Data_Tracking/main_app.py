#This file will be for the main application section of the stock data scraper

#Imports
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QPushButton,
    QLabel, QVBoxLayout, QHBoxLayout,
    QLineEdit, QWidget
)

from PyQt6.QtCore import QMutex, QThread, pyqtSignal
from PyQt6.QtGui import QFont

import sys, os

MAIN_FONT = QFont()
MAIN_FONT.setPointSize(14)

class MainWindow(QMainWindow):
    #Create get stock info layout
    def createGetStockDataLayout(self):
        self.is_scraping = False
        stock_abbr_label = QLabel("Stock Abbriviation")
        stock_abbr_label.setFont(MAIN_FONT)
        self.stock_abbr_input = QLineEdit()
        self.stock_abbr_input.setFont(MAIN_FONT)
        self.stock_abbr_input.textChanged.connect(self.capitilizeStockInput)
        self.stock_abbr_input.returnPressed.connect(self.startScrape)
        self.start_scrape_button = QPushButton("Start")
        self.start_scrape_button.setFont(MAIN_FONT)
        self.start_scrape_button.clicked.connect(self.startScrape)

        getStockDataLayout = QHBoxLayout()
        getStockDataLayout.addWidget(stock_abbr_label)
        getStockDataLayout.addWidget(self.stock_abbr_input)
        getStockDataLayout.addWidget(self.start_scrape_button)

        return getStockDataLayout

    #Change output folder layout
    def createSetOutputFolderLayout(self):
        self.output_folder_line = QLineEdit()
        self.output_folder_line.setReadOnly(True)
        self.output_folder_line.setFont(MAIN_FONT)
        change_output_button = QPushButton("Select Folder")
        change_output_button.setFont(MAIN_FONT)
        change_output_button.clicked.connect(self.changeOutputFolder)
        
        change_output_folder_Layout = QHBoxLayout()
        change_output_folder_Layout.addWidget(self.output_folder_line)
        change_output_folder_Layout.addWidget(change_output_button)
        
        return change_output_folder_Layout

    #Create scrape info relay layout
    def createRelayLayout(self):
        self.scrape_info_label = QLabel("Scraping status: None")
        self.scrape_info_label.setFont(MAIN_FONT)
        
        email_logs_label = QLabel("Email me logs")
        email_logs_label.setFont(MAIN_FONT)
        self.email_logs_button = QPushButton("Send")
        self.email_logs_button.setFont(MAIN_FONT)
        self.email_logs_button.setEnabled(False)
        
        final_layout = QVBoxLayout()
        logs_layout = QHBoxLayout()
        
        logs_layout.addWidget(email_logs_label)
        logs_layout.addWidget(self.email_logs_button)
        
        final_layout.addWidget(self.scrape_info_label)
        final_layout.addLayout(logs_layout)
        return final_layout

    def __init__(self):
        super(MainWindow, self).__init__()
        self.setWindowTitle("Yahoo Stock Data Scraper")

        main_layout = QVBoxLayout()
        main_widget = QWidget()

        pull_stock_layout = self.createGetStockDataLayout()
        output_folder_layout = self.createSetOutputFolderLayout()
        info_layout = self.createRelayLayout()
        
        main_layout.addLayout(pull_stock_layout)
        main_layout.addLayout(output_folder_layout)
        main_layout.addLayout(info_layout)
        main_widget.setLayout(main_layout)
        self.setCentralWidget(main_widget)


    # ---------------------
    # Functional methods
    # ---------------------
    
    def capitilizeStockInput(self):
        self.stock_abbr_input.setText(self.stock_abbr_input.text().upper())
        
    def startScrape(self): 
        if not self.stock_abbr_input.text() or self.is_scraping:
            
            return False
        
        self.is_scraping = True
        self.start_scrape_button.setEnabled(False)
        abbr = self.stock_abbr_input.text()

    def changeOutputFolder(self):
        pass
            
    def email_logs(self):
        pass
    
if __name__ == "__main__":
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec()