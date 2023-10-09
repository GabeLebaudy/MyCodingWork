#Import modules
from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6.QtCore import Qt
import datetime

class TableModel(QtCore.QAbstractTableModel):
    #Constructor
    def __init__ (self, data):
        super(TableModel, self).__init__()
        self.tableData = data
        
    def data(self, index, role): #Must be named data or 
        if role == Qt.ItemDataRole.DisplayRole:
            #Get the value of the data
            value = self.tableData[index.row()][index.column()]
            
            if isinstance(value, datetime.datetime):
                return value.strftime("%m-%d-%Y")
            
            if isinstance(value, float):
                return "%.2f" % value
            
            if isinstance(value, str):
                return '"%s"' % value
            
            #Default: I.e. int or bool
            return value
            
        
    def rowCount(self, index):
        return len(self.tableData) #Number of data lists in the data
    
    def columnCount(self, index):
        return len(self.tableData[0]) #Takes the first sub-list and returns its length. This only works when all rows are the same length
    
class MainWindow(QtWidgets.QMainWindow):
    #Constructor method
    def __init__(self):
        super().__init__()
        
        self.tableWidget = QtWidgets.QTableView() #Create table widget (Shell of table with no data)
        
        data = [ #Data structure
            [4, 9, 2],
            [1, -1, 'hello'],
            [3.023, 5, -5],
            [3, 3, datetime.datetime(2017, 10, 1)],
            [7.555, 8, 9]
        ]
        
        self.tableModel = TableModel(data) #Create table data obj (imagine the data is tabeled, but no table to put it in)
        self.tableWidget.setModel(self.tableModel) #Sets table data to the table model (Abstract table data)
        
        self.setCentralWidget(self.tableWidget)
        
if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    
    window = MainWindow()
    window.show()
    
    app.exec()