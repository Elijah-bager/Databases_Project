import sqlite3

# Connect to (or create) the database
connection = sqlite3.connect('my_database.db')
cursor = connection.cursor()

# Read the SQL script from create.txt
with open('3241CreateM2.txt', 'r') as file:
    sql_script = file.read()

# Execute the script
cursor.executescript(sql_script)

# Save changes and close
connection.commit()

# Populate the database
with open('3241PopulateM2.txt', 'r') as file:
    sql_script = file.read()
cursor.executescript(sql_script)

connection.commit()

# Execute the query to retrieve all records from the Users table
for row in cursor.execute("SELECT * FROM User"):
    print(row)

connection.close()
