#This file will be used to test out the connection between SQL and Python using pypyodbc

#Imports
import pypyodbc as odbc

SERVER_NAME = "DESKTOP-KPNI5SV\SQLEXPRESS"
DRIVER_NAME = 'SQL SERVER'
DATABASE_NAME = 'testing'

connect = """
    DRIVER={{{DRIVER_NAME}}};
    SERVER={SERVER_NAME};
    DATABASE={DATABASE_NAME};
    Trust_Connection=yes;
"""

sql_conn = odbc.connect(connect)
print(sql_conn)

