#This file will be used to test out the connection between SQL and Python using pypyodbc

#Imports
import pypyodbc as odbc

SERVER_NAME = "LPD-17\SQLEXPRESS"
DRIVER_NAME = 'SQL SERVER'
DATABASE_NAME = 'Network_Provider_Stream_Data'


class ServerConnection():
    #Constructor
    def __init__(self):        
        connect = """
            DRIVER={{{DRIVER_NAME}}};
            SERVER={SERVER_NAME};
            DATABASE={DATABASE_NAME};
            Trust_Connection=yes;
        """.format(DRIVER_NAME=DRIVER_NAME, SERVER_NAME=SERVER_NAME, DATABASE_NAME=DATABASE_NAME)

        self.sql_conn = odbc.connect(connect)
        self.cursor = self.sql_conn.cursor()

    #Pull the data from the areas table to search for on the website
    def getAreaData(self):
        pass

    #Check the providers table if the provider is present. If not, add it to the table.
    def verifyProvider(self, provider):
        pass

    #Add an entry to the full data table.
    def addFullDataEntry(self, city, state, provider_name, date, definition, streaming_data, vol_chart_path, per_chart_path):
        pass

    #Close the connection to the server if the program has an unexpected problem
    def closeConnection(self):
        self.cursor.close()
        self.sql_conn.close()

