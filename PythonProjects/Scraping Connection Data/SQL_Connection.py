#This file will be used to test out the connection between SQL and Python using pypyodbc

#Imports
import pypyodbc as odbc
from datetime import datetime
import random, os, sys

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
        #Query database for all cities, and the state code
        get_all_areas_query = "select * from Areas;"
        self.cursor.execute(get_all_areas_query)
        all_areas = self.cursor.fetchall()
        
        #Convert all tuples into a single string
        website_strings = []
        for area in all_areas:
            website_strings.append("{}, {}".format(area[0], area[1]))
        
        return website_strings

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
        #Generate the insert statement for adding a row to the database
        if city:
            full_query = "insert into network_streaming_data(city, state, date_retrieved, youtube_assigned_definition,"
        else:
            full_query = "insert into network_streaming_data(state, date_retrieved, youtube_assigned_definition,"

        full_query += self.genColumns()

        date = datetime.today().strftime('%Y-%m-%d')

        if city:
            if vol_chart_path and per_chart_path:
                full_query += "vol_chart, per_chart, provider) values ('{}', '{}', '{}', '{}', ".format(city, state, date, definition)
            else:
                full_query += "provider) values ('{}', '{}', '{}', '{}', ".format(city, state, date, definition)
        else:
            if vol_chart_path and per_chart_path:
                full_query += "vol_chart, per_chart, provider) values ('{}', '{}', '{}', ".format(state, date, definition)
            else:
                full_query += "provider) values ('{}', '{}', '{}', ".format(state, date, definition)
        
        for i in range(len(streaming_data)):
            full_query += "{}, ".format(streaming_data[i])
        
        #Smooth handling in case images were unable to be captured. 
        if vol_chart_path and per_chart_path:
            full_query += "(Select * from Openrowset (BULK '{}', Single_blob) as T), (Select * from Openrowset (BULK '{}', Single_blob) as T), '{}')".format(vol_chart_path, per_chart_path, provider_name)
        else:
            full_query += "'{}')".format(provider_name)
                
        self.cursor.execute(full_query)
        self.sql_conn.commit()
        
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

