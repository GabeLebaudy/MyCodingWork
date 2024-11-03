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
        stock_abbr_label = QLabel("Stock Abbriviation")
        stock_abbr_label.setFont(MAIN_FONT)
        self.stock_abbr_input = QLineEdit()
        start_scrape_button = QPushButton("Start")

        getStockDataLayout = QHBoxLayout()
        getStockDataLayout.addWidget(stock_abbr_label)
        getStockDataLayout.addWidget(self.stock_abbr_input)
        getStockDataLayout.addWidget(start_scrape_button)

        return getStockDataLayout

    #Change output folder layout
    def createSetOutputFolderLayout(self):
        pass

    #Create scrape info relay layout
    def createRelayLayout(self):
        pass

    def __init__(self):
        super(MainWindow, self).__init__()
        self.setWindowTitle("Yahoo Stock Data Scraper")

        main_layout = QVBoxLayout()
        main_widget = QWidget()

        pull_stock_layout = self.createGetStockDataLayout()

        main_layout.addLayout(pull_stock_layout)
        main_widget.setLayout(main_layout)
        self.setCentralWidget(main_widget)

if __name__ == "__main__":
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec()