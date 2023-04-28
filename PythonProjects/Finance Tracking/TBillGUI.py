#This will be the file that contains the gui that has the visualiziation of the T_Bill data plus controls to focus on one aspect of it

#Import modules
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os
import math
from PyQt6.QtWidgets import (
    QPushButton, QMainWindow, QApplication,
    QLineEdit, QLabel, QSpinBox,
    QDoubleSpinBox, QFileDialog, QDialog,
    QVBoxLayout, QHBoxLayout, QGridLayout,
    QWidget
)
from PyQt6.QtCore import Qt
from testGraphT_BillRates import TBillGraph
#Main window subclass

class MainWindow(QMainWindow):
    #Constructor
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setWindowTitle("T-Bill Data Mod")

        #Main layout will be layout of central widget, first section is layout container for this first part
        self.MainLayout = QHBoxLayout()
        self.firstSection = QVBoxLayout()

        self.graphButtons = QGridLayout()

        self.buttonLabels = [
                            '4 Week Bank Discount', '4 Week Coupon Equivalent', '8 Week Bank Discount', '8 Week Coupon Equivalent', 
                             '13 Week Bank Discount', '13 Week Coupon Equivalent', '17 Week Bank Discount', '17 Week Coupon Equivalent',
                             '26 Week Bank Discount', '26 Week Coupon Equivalent', '52 Week Bank Discount', '52 Week Coupon Equivalent'
                             ]
        #Loop that creates buttons
        self.termButtonArray = []
        leftRight = 0
        for i in range(len(self.buttonLabels)):
            btnTxt = self.buttonLabels[i]
            newButton = QPushButton(btnTxt)
            newButton.setCheckable(True)
            if i % 2 == 0:
                newButton.setChecked(True)
            else:
                newButton.setChecked(False)
            newButton.clicked.connect(lambda checked, text=btnTxt: self.toggleTerm(text, checked))
            self.graphButtons.addWidget(newButton, i // 2, leftRight)
            self.termButtonArray.append([newButton])
            if leftRight == 0:
                leftRight = 1
            else:
                leftRight = 0
    
        self.TBillGraph = TBillGraph()
        self.firstSection.addLayout(self.graphButtons)
        self.firstSection.addWidget(self.TBillGraph)
        self.TBillGraph.drawGraph()


        self.MainLayout.addLayout(self.firstSection)

        self.container = QWidget()
        self.container.setLayout(self.MainLayout)

        self.setCentralWidget(self.container)

        self.TBillGraph.draw()


    #Updates graph with new parameters
    def updateGraph(self, graph):
        graph.drawGraph()
        graph.draw()

    def toggleTerm(self, text, isChecked):
        splitTxt = text.split(' ')
        termLength = splitTxt[0]
        bankOrCoupon = splitTxt[2]
        if isChecked is True:
            self.TBillGraph.enableTerm(int(termLength), bankOrCoupon)
        else:
            self.TBillGraph.disableTerm(int(termLength), bankOrCoupon)
        
        self.updateGraph(self.TBillGraph)

#Main Script
if __name__ == "__main__":
    app = QApplication([])

    window = MainWindow()
    window.show()

    app.exec()


