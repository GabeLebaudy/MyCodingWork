#This file will be used to store constant values. These values will never change, so they don't need to be in the code, they will just be defined once here.

#Imports
from PyQt6.QtWidgets import (
    QSpacerItem, QSizePolicy
)

#Some Sample Spacer Items
EXPANDINGHORIZONTAL = QSpacerItem(0, 0, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)
EXPANDINGVERTICAL = QSpacerItem(0, 0, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)


#Style Sheet
HELPBUTTONSTYLE = '''
                QPushButton {
                border: 2px solid #000000;
                border-radius: 20px; /* Set to half the button size for a perfect circle */
                background-color: #dcdde0;
                color: #000000;
                padding: 6px; /* Adjust padding as needed */
                }
                QPushButton:hover {
                    background-color: #EAEAEA; /* Change color on hover */
                }
                '''

QUEUEBUTTONSTYLE = '''
                QPushButton {
                border: 2px solid #000000;
                border-radius: 15px; /* Set to half the button size for a perfect circle */
                background-color: #dcdde0;
                color: #000000;
                padding: 6px; /* Adjust padding as needed */
                }
                QPushButton:hover {
                    background-color: #EAEAEA; /* Change color on hover */
                }
                '''