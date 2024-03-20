#This file will be used to test out the connection between SQL and Python using pypyodbc

#Imports
import pypyodbc as odbc
from datetime import datetime
import random

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
        get_all_areas_query = "select * from Areas;"
        self.cursor.execute(get_all_areas_query)
        all_areas = self.cursor.fetchall()
        return all_areas

    #Check the providers table if the provider is present. If not, add it to the table.
    def verifyProvider(self, provider):
        verification_query = "select provider_name from providers where provider_name = '{}';".format(provider)
        self.cursor.execute(verification_query)
        row = self.cursor.fetchall()

        if not row:
            input_query = "insert into providers (provider_name) values ('{}');".format(provider)
            self.cursor.execute(input_query)
            self.sql_conn.commit()

    #Add an entry to the full data table.
    def addFullDataEntry(self, city, state, provider_name, definition, streaming_data, vol_chart_path, per_chart_path):
        full_query = "insert into network_streaming_data(city, state, date_retrieved, youtube_assigned_definition,"
        full_query += self.genColumns()

        date = datetime.today().strftime('%Y-%m-%d')

        full_query += "volchart, per_chart, provider) values ('{}', '{}', '{}', '{}', ".format(city, state, date, definition)
        
        for i in range(len(streaming_data)):
            full_query += "{}, ".format(streaming_data[i])
        
        full_query += "?, ?, {})".format(provider_name)
        
        print(full_query)
        

    #Generate the hd_stream_columns
    def genColumns(self):
        full_str, am_or_pm, counter = "", "AM", 5
        for i in range(24):
            counter += 1
            if counter == 12:
                if am_or_pm == "AM":
                    am_or_pm = "PM"
                else:
                    am_or_pm = "AM"
                
                string_to_add = "hd_streams_{}, ".format(str(counter) + am_or_pm)
                counter = 0

            else:
                string_to_add = "hd_streams_{}, ".format(str(counter) + am_or_pm)

            full_str += string_to_add

        return full_str

    #Close the connection to the server if the program has an unexpected problem
    def closeConnection(self):
        self.cursor.close()
        self.sql_conn.close()


if __name__ == "__main__":
    sql_conn = ServerConnection()
    data = []
    for i in range(24):
        data.append(90 + random.randint(1, 8))

    sql_conn.addFullDataEntry("Philadelphia", "PA", "Xfinity", 'HD', data, None, None)
