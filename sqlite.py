import sqlite3

### Connect to Sqlite if this database doses exit it create

connection = sqlite3.connect('student.db')

## create a cursor object to insert record,create table

cursor=connection.cursor()

## Create a Table
table_info="""

CREATE TABLE STUDENT(
            NAME VARCHAR(25),
            CLASS VARCHAR(25),
            AGE INT
)

"""
cursor.execute(table_info)

## Insert Some Record

cursor.execute('''INSERT INTO STUDENT VALUES("Ashutosh Singh","Data Science",25)''')
cursor.execute('''INSERT INTO STUDENT VALUES("Shivam","Andriod developer",27)''')
cursor.execute('''INSERT INTO STUDENT VALUES("akash","Deveops",22)''')
cursor.execute('''INSERT INTO STUDENT VALUES("kartikey","Data Science",24)''')



## Displat  all the records

print("The Inserted records are ")
data=cursor.execute(""" SELECT * FROM STUDENT """) 
for row in data:
    print(row)

### commit your changes in the database
connection.commit()
connection.close()