import mysql.connector

# Connect to MySQL database (replace with your MySQL details)
connection = mysql.connector.connect(
    host="localhost",  # Your MySQL server host (e.g., 'localhost' or an IP address)
    user="root",       # Your MySQL username
    password="root",   # Your MySQL password
    database="hello"  # The database to connect to (replace with your database name)
)

# Create a cursor object to insert record, create table
cursor = connection.cursor()

# Create the table (if not exists)
table_info = """
CREATE TABLE IF NOT EXISTS STUDENT(
    NAME VARCHAR(25),
    CLASS VARCHAR(25),
    SECTION VARCHAR(25),
    MARKS INT
)
"""

cursor.execute(table_info)

# Insert records
cursor.execute("INSERT INTO STUDENT (NAME, CLASS, SECTION, MARKS) VALUES ('Krish', 'Data Science', 'A', 90)")
cursor.execute("INSERT INTO STUDENT (NAME, CLASS, SECTION, MARKS) VALUES ('John', 'Data Science', 'B', 100)")
cursor.execute("INSERT INTO STUDENT (NAME, CLASS, SECTION, MARKS) VALUES ('Mukesh', 'Data Science', 'A', 86)")
cursor.execute("INSERT INTO STUDENT (NAME, CLASS, SECTION, MARKS) VALUES ('Jacob', 'DEVOPS', 'A', 50)")
cursor.execute("INSERT INTO STUDENT (NAME, CLASS, SECTION, MARKS) VALUES ('Dipesh', 'DEVOPS', 'A', 35)")

# Display all the records
print("The inserted records are:")
cursor.execute("SELECT * FROM STUDENT")
for row in cursor.fetchall():
    print(row)

# Commit your changes to the database
connection.commit()

# Close the connection
connection.close()
