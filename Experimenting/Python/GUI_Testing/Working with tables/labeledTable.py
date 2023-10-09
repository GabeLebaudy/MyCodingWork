#Import modules
from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6.QtCore import Qt
import pandas as pd

#Table data (Model) class
class TableModel(QtCore.QAbstractTableModel):
    #Constructor
    def __init__(self, data):
        super().__init__()
        self.tableData = data
        
    def data(self, index, role):
        if role == Qt.ItemDataRole.DisplayRole:
            value = self.tableData.iloc[index.row(), index.column()]
            return "%.2f" % value
        
    def rowCount(self, index):
        return self.tableData.shape[0]
    
    def columnCount(self, index):
        return self.tableData.shape[1]
    
    def headerData(self, section, orientation, role):
        if role == Qt.ItemDataRole.DisplayRole:
            if orientation == Qt.Orientation.Horizontal:
                return str(self.tableData.columns[section])
            
            if orientation == Qt.Orientation.Vertical:
                return str(self.tableData.index[section])
            
class MainWindow(QtWidgets.QMainWindow):
    #Constructor
    def __init__(self):
        super().__init__()
        
        self.tableShell = QtWidgets.QTableView()
        
        data = pd.DataFrame( 
        [
            [1, 9, 2],
            [1, 0, -1],
            [3, 5, 2],
            [3, 5, 2],
            [5, 8, 9]
        ], columns = ['A', 'B', 'C',], index = ['Row 1', 'Row 2', 'Row 3', 'Row 4', 'Row 5']    
        )
        
        self.tableModel = TableModel(data)
        self.tableShell.setModel(self.tableModel)
        
        self.setCentralWidget(self.tableShell)
        
        
        
if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    
    window = MainWindow()
    window.show()
    
    app.exec()