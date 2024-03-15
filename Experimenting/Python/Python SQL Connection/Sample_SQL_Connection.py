#This file will be used to test out the connection between SQL and Python using pypyodbc

#Imports
import pypyodbc as odbc

SERVER_NAME = "LPD-17\SQLEXPRESS"
DRIVER_NAME = 'SQL SERVER'
DATABASE_NAME = 'testing_sql'

connect = """
    DRIVER={{{DRIVER_NAME}}};
    SERVER={SERVER_NAME};
    DATABASE={DATABASE_NAME};
    Trust_Connection=yes;
""".format(DRIVER_NAME=DRIVER_NAME, SERVER_NAME=SERVER_NAME, DATABASE_NAME=DATABASE_NAME)

sql_conn = odbc.connect(connect)

select_query = "SELECT * FROM simple_table;"

cursor = sql_conn.cursor()
cursor.execute(select_query)

row = cursor.fetchone()

if row:
    print("ID: {}".format(row[0]))
    print("Occupation: {}".format(row[1]))

else:
    print("SQL Fetch Failed")

cursor.close()
sql_conn.close()

