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
    QWidget, QComboBox, QCheckBox,
    QSpacerItem, QSizePolicy
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

        self.topContainer = QHBoxLayout()
        
        self.pickYear = QVBoxLayout()
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
            newButton.setMaximumSize(175, 50)
            newButton.clicked.connect(lambda checked, text=btnTxt: self.toggleTerm(text, checked))
            self.graphButtons.addWidget(newButton, i // 2, leftRight)
            self.termButtonArray.append([newButton])
            if leftRight == 0:
                leftRight = 1
            else:
                leftRight = 0

        self.graphButtons.setAlignment(Qt.AlignmentFlag.AlignLeft)
        
        #Create Time controls widgets
        self.disableAllCouponsLabel = QLabel('Disable Coupon Equivalent Lines')
        self.disableAllCouponsCB = QCheckBox()
        self.startDateLabel = QLabel("Start Date:")
        self.startDateInput = QLineEdit()
        self.stopDateLabel = QLabel("Stop Date:")
        self.stopDateInput = QLineEdit()
        self.pickYearLabel = QLabel('Show whole year:')
        self.pickYearBox = QComboBox()
        
        self.disableAllCouponsCB.setChecked(True)
        self.pickYearBox.addItems([
                                    '2023', '2022', '2021', '2020', '2019', '2018', '2017', '2016', '2015',
                                    '2014', '2013', '2012', '2011', '2010', '2009', '2008', '2007', '2006',
                                    '2005', '2004', '2003', '2002'
                                   ])
        
        self.pickYearBox.currentTextChanged.connect(self.loadNewYear)
        
        #Sub-layouts
        self.controlsLayout = QVBoxLayout()
        self.disableCouponsLayout = QHBoxLayout()
        self.timeManipulationLayout = QHBoxLayout()
        
        #Add widgets to layout 
        self.disableCouponsLayout.addWidget(self.disableAllCouponsCB)
        self.disableCouponsLayout.addWidget(self.disableAllCouponsLabel)
        
        self.timeManipulationLayout.addWidget(self.startDateLabel)
        self.timeManipulationLayout.addWidget(self.startDateInput)
        
        self.timeManipulationLayout.addWidget(self.stopDateLabel)
        self.timeManipulationLayout.addWidget(self.stopDateInput)
        
        self.timeManipulationLayout.addWidget(self.pickYearLabel)
        self.timeManipulationLayout.addWidget(self.pickYearBox)
        
        self.disableCouponsLayout.setAlignment(Qt.AlignmentFlag.AlignLeft)        
        self.timeManipulationLayout.setAlignment(Qt.AlignmentFlag.AlignLeft)
        
        self.controlsLayout.addLayout(self.disableCouponsLayout)
        self.controlsLayout.addSpacerItem(QSpacerItem(0, 0, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding))
        self.controlsLayout.addLayout(self.timeManipulationLayout)
        
        self.controlsLayout.setAlignment(Qt.AlignmentFlag.AlignTop)
        
        self.topContainer.addLayout(self.graphButtons)
        self.topContainer.addLayout(self.controlsLayout)
        
        self.topContainer.setAlignment(Qt.AlignmentFlag.AlignBaseline)
        
        self.TBillGraph = TBillGraph()
        self.firstSection.addLayout(self.topContainer)
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
        
    def loadNewYear(self, year):
        self.TBillGraph.loadWholeYear(year)
        #TODO: Use if statements to figure out which years have which term lengths. It seems like 2021 and before don't have 17 week ones, probably they are a recent edition.
        #2021, 6--5 2017 5--4, 2007 4---3, 2002 3--4
        self.updateGraph(self.TBillGraph)

#Main Script
if __name__ == "__main__":
    app = QApplication([])

    window = MainWindow()
    window.show()

    app.exec()


