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

        self.monthWeekBank = QPushButton("4 Week Bank Discount")
        self.monthWeekCoupon = QPushButton("4 Week Coupon Equivalent")

        self.biMonthWeekBank = QPushButton("8 Week Bank Discount")
        self.biMonthWeekCoupon = QPushButton("8 Week Coupon Equivalent")

        self.triMonthWeekBank = QPushButton("13 Week Bank Discount")
        self.triMonthWeekCoupon = QPushButton("13 Week Coupon Equivalent")

        self.quadMonthWeekBank = QPushButton("17 Week Bank Discount")
        self.quadMonthWeekCoupon = QPushButton("17 Week Coupon Equivalent")

        self.halfYearBank = QPushButton("26 Week Bank Discount")
        self.halfyearCoupon = QPushButton("26 Week Coupon Equivalent")

        self.fullYearBank = QPushButton("52 Week Bank Discount")
        self.fullYearCoupon = QPushButton("52 Week Coupon Equivalent")

        self.graphButtons.addWidget(self.monthWeekBank, 0, 0)
        self.graphButtons.addWidget(self.monthWeekCoupon, 0, 1)

        self.graphButtons.addWidget(self.biMonthWeekBank, 1, 0)
        self.graphButtons.addWidget(self.biMonthWeekCoupon, 1, 1)

        self.graphButtons.addWidget(self.triMonthWeekBank, 2, 0)
        self.graphButtons.addWidget(self.triMonthWeekCoupon, 2, 1)

        self.graphButtons.addWidget(self.quadMonthWeekBank, 3, 0)
        self.graphButtons.addWidget(self.quadMonthWeekCoupon, 3, 1)

        self.graphButtons.addWidget(self.halfYearBank, 4, 0)
        self.graphButtons.addWidget(self.halfyearCoupon, 4, 1)

        self.graphButtons.addWidget(self.fullYearBank, 5, 0)
        self.graphButtons.addWidget(self.fullYearCoupon, 5, 1)

        self.TBillGraph = TBillGraph()
        self.firstSection.addLayout(self.graphButtons)
        self.firstSection.addWidget(self.TBillGraph)
        self.TBillGraph.drawGraph()


        self.MainLayout.addLayout(self.firstSection)

        self.container = QWidget()
        self.container.setLayout(self.MainLayout)

        self.setCentralWidget(self.container)

        self.TBillGraph.draw()

#Main Script
if __name__ == "__main__":
    app = QApplication([])

    window = MainWindow()
    window.show()

    app.exec()


