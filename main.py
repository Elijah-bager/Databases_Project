import os
import sqlite3

# # Connect to (or create) the database
# connection = sqlite3.connect('my_database.db')
# cursor = connection.cursor()

# # Read the SQL script from create.txt
# with open('3241CreateM2.txt', 'r') as file:
#     sql_script = file.read()

# # Execute the script
# cursor.executescript(sql_script)

# # Save changes and close
# connection.commit()

# # Populate the database
# with open('3241PopulateM2.txt', 'r') as file:
#     sql_script = file.read()
# cursor.executescript(sql_script)

# connection.commit()

# # Execute the query to retrieve all records from the Users table
# for row in cursor.execute("SELECT * FROM User"):
#     print(row)

# connection.close()
class query:
    def __init__(self,connection):
        self.connection = connection
        self.cursor = self.connection.cursor()
        self.query_one = ""
        self.query_two = ""
        self.query_three = ""
    def execute_query_one(self):
        self.query_one = "SELECT u.Name, w.DateTime, e.name AS ExerciseName, " \
        " sd.Weight FROM User u JOIN Workout w ON u.Id = w.UserId " \
        "JOIN WorkoutExercise we ON w.Id = we.WorkoutId " \
        "JOIN Exercise e ON we.ExerciseId = e.Id JOIN StrengthDetails sd ON " \
        "we.Id = sd.WorkoutExerciseId WHERE sd.Weight > 100;"
        self.cursor.execute(self.query_one)
        results = self.cursor.fetchall()
        for row in results:
            print(row)
    def execute_query_two(self):
        self.query_two = "SELECT mg.Name AS MuscleGroupName, " \
        "e.Name AS ExerciseName FROM MuscleGroup mg " \
        "JOIN ExerciseMuscleGroup emg ON mg.Id = emg.MuscleGroupId " \
        "JOIN Exercise e ON emg.ExerciseId = e.Id ORDER BY mg.Name, e.Name;"
        self.cursor.execute(self.query_two)
        results = self.cursor.fetchall()
        for row in results:
            print(row)
    def execute_query_three(self):
        self.query_three = """
    SELECT u.Id, u.Name, SUM(cd.Distance) AS TotalDistance
    FROM User u
    JOIN Workout w ON u.Id = w.UserId
    JOIN WorkoutExercise we ON w.Id = we.WorkoutId
    JOIN CardioDetails cd ON we.Id = cd.WorkoutExerciseId
    GROUP BY u.Id, u.Name
    ORDER BY TotalDistance DESC;
    """
        self.cursor.execute(self.query_three)
        results = self.cursor.fetchall()
        for row in results:
            print(row)
def main():
    # Remove any existing database file so this run starts fresh
    db_path = 'my_database.db'
    if os.path.exists(db_path):
        os.remove(db_path)

    # Connect to a fresh database
    connection = sqlite3.connect(db_path)
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

    q = query(connection)
    while True:
        print("\nWhich query would you like to run?")
        print("1. Users who lifted more than 100 pounds")
        print("2. Muscle groups and their exercises")
        print("3. Total distance covered by each user")
        print("4. Exit")

        choice = input("Enter your choice: ")

        if choice == "1":
            print("\nQuery 1: Users who lifted more than 100 pounds:")
            q.execute_query_one()

        elif choice == "2":
            print("\nQuery 2: Muscle groups and their exercises:")
            q.execute_query_two()

        elif choice == "3":
            print("\nQuery 3: Total distance covered by each user:")
            q.execute_query_three()

        elif choice == "4":
            print("Exiting program.")
            break

        else:
            print("Invalid choice. Please enter 1, 2, 3, or 4.")

    connection.close()
if __name__ == "__main__":    main()