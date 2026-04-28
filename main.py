import os
import datetime
import sqlite3


class query:
    def __init__(self, connection):
        self.connection = connection
        self.cursor = self.connection.cursor()
        self.query_one = ""
        self.query_two = ""
        self.query_three = ""

    def _prompt_non_empty(self, prompt: str) -> str:
        while True:
            value = input(prompt).strip()
            if value:
                return value
            print("Input cannot be empty.")

    def _prompt_int(self, prompt: str, *, min_value=None) -> int:
        while True:
            raw = input(prompt).strip()
            try:
                value = int(raw)
            except ValueError:
                print("Please enter a valid integer.")
                continue
            if min_value is not None and value < min_value:
                print(f"Please enter an integer >= {min_value}.")
                continue
            return value

    def _prompt_float(self, prompt: str, *, min_value=None) -> float:
        while True:
            raw = input(prompt).strip()
            try:
                value = float(raw)
            except ValueError:
                print("Please enter a valid number.")
                continue
            if min_value is not None and value < min_value:
                print(f"Please enter a number >= {min_value}.")
                continue
            return value

    def _print_single_row(self, sql: str, params: tuple):
        self.cursor.execute(sql, params)
        row = self.cursor.fetchone()
        print(row)

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

    def execute_query_four(self):
        self.cursor.execute(
            "SELECT Id, Name, "
            "CASE WHEN Type = 'Cardio' THEN 'Endurance' ELSE Type END AS ExerciseType "
            "FROM Exercise ORDER BY Id;"
        )
        results = self.cursor.fetchall()
        for row in results:
            print(row)

    def execute_query_five(self):
        user_id = self._prompt_int("UserId: ", min_value=1)

        self.cursor.execute(
            "SELECT Name, Email FROM User WHERE Id = ?", (user_id,))
        user_row = self.cursor.fetchone()
        if user_row is None:
            print("No user found with that UserId.")
            return

        print(f"Workouts for User {user_id} ({user_row[0]}, {user_row[1]}):")
        self.cursor.execute(
            "SELECT Id, DateTime FROM Workout WHERE UserId = ? ORDER BY DateTime;",
            (user_id,),
        )
        results = self.cursor.fetchall()
        if not results:
            print("(no workouts found for this user)")
            return
        for row in results:
            print(row)

    def add_user(self):
        print("\nAdd User")
        name = self._prompt_non_empty("Name: ")
        email = self._prompt_non_empty("Email: ")
        password = self._prompt_non_empty("Password: ")
        age = self._prompt_int("Age: ", min_value=1)
        weight = self._prompt_float("Weight: ", min_value=0.000001)
        height = self._prompt_float("Height: ", min_value=0.000001)
        join_date = datetime.date.today().isoformat()

        self.cursor.execute(
            "INSERT INTO User (Name, Email, Password, Age, Weight, Height, JoinDate) VALUES (?, ?, ?, ?, ?, ?, ?)",
            (name, email, password, age, weight, height, join_date),
        )
        user_id = self.cursor.lastrowid
        self.connection.commit()

        print("\nCreated User row:")
        self._print_single_row("SELECT * FROM User WHERE Id = ?", (user_id,))

    def add_workout(self):
        print("\nAdd Workout")
        user_id = self._prompt_int("UserId: ", min_value=1)
        self.cursor.execute("SELECT 1 FROM User WHERE Id = ?", (user_id,))
        if self.cursor.fetchone() is None:
            print("No user found with that UserId.")
            return

        datetime_str = self._prompt_non_empty(
            "Workout DateTime (YYYY-MM-DD HH:MM): ")

        self.cursor.execute(
            "INSERT INTO Workout (UserId, DateTime) VALUES (?, ?)",
            (user_id, datetime_str),
        )
        workout_id = self.cursor.lastrowid
        self.connection.commit()

        print("Created Workout row:")
        self._print_single_row(
            "SELECT * FROM Workout WHERE Id = ?", (workout_id,))

    def add_exercise_to_workout(self):
        print("\nAdd Exercise To Workout")
        workout_id = self._prompt_int("WorkoutId: ", min_value=1)
        self.cursor.execute(
            "SELECT 1 FROM Workout WHERE Id = ?", (workout_id,))
        if self.cursor.fetchone() is None:
            print("No workout found with that WorkoutId.")
            return

        exercise_id = self._prompt_int("ExerciseId: ", min_value=1)
        self.cursor.execute(
            "SELECT Type FROM Exercise WHERE Id = ?", (exercise_id,))
        ex_row = self.cursor.fetchone()
        if ex_row is None:
            print("No exercise found with that ExerciseId.")
            return
        exercise_type = ex_row[0]

        self.cursor.execute(
            "INSERT INTO WorkoutExercise (WorkoutId, ExerciseId) VALUES (?, ?)",
            (workout_id, exercise_id),
        )
        workout_exercise_id = self.cursor.lastrowid

        if exercise_type == "Strength":
            sets = self._prompt_int("Sets: ", min_value=1)
            reps = self._prompt_int("Reps: ", min_value=1)
            weight = self._prompt_float("Weight: ", min_value=0.000001)
            self.cursor.execute(
                "INSERT INTO StrengthDetails (WorkoutExerciseId, Sets, Reps, Weight) VALUES (?, ?, ?, ?)",
                (workout_exercise_id, sets, reps, weight),
            )
        else:
            duration = self._prompt_float("Duration: ", min_value=0.000001)
            distance = self._prompt_float("Distance: ", min_value=0.000001)
            self.cursor.execute(
                "INSERT INTO CardioDetails (WorkoutExerciseId, Duration, Distance) VALUES (?, ?, ?)",
                (workout_exercise_id, duration, distance),
            )

        self.connection.commit()

        print("Created WorkoutExercise row:")
        self._print_single_row(
            "SELECT * FROM WorkoutExercise WHERE Id = ?", (workout_exercise_id,))
        if exercise_type == "Strength":
            print("Created StrengthDetails row:")
            self._print_single_row(
                "SELECT * FROM StrengthDetails WHERE WorkoutExerciseId = ?",
                (workout_exercise_id,),
            )
        else:
            print("Created CardioDetails row:")
            self._print_single_row(
                "SELECT * FROM CardioDetails WHERE WorkoutExerciseId = ?",
                (workout_exercise_id,),
            )

    def get_workout_info(self):
        print("\nGet Workout Info")
        workout_id = self._prompt_int("WorkoutId: ", min_value=1)

        self.cursor.execute(
            "SELECT w.Id, w.DateTime, u.Id, u.Name, u.Email "
            "FROM Workout w JOIN User u ON u.Id = w.UserId "
            "WHERE w.Id = ?",
            (workout_id,),
        )
        header = self.cursor.fetchone()
        if header is None:
            print("No workout found with that WorkoutId.")
            return
        print("Workout (WorkoutId, DateTime, UserId, UserName, UserEmail):")
        print(header)

        self.cursor.execute(
            "SELECT we.Id AS WorkoutExerciseId, e.Id AS ExerciseId, e.Name, e.Type, "
            "sd.Sets, sd.Reps, sd.Weight, cd.Duration, cd.Distance "
            "FROM WorkoutExercise we "
            "JOIN Exercise e ON e.Id = we.ExerciseId "
            "LEFT JOIN StrengthDetails sd ON sd.WorkoutExerciseId = we.Id "
            "LEFT JOIN CardioDetails cd ON cd.WorkoutExerciseId = we.Id "
            "WHERE we.WorkoutId = ? "
            "ORDER BY we.Id",
            (workout_id,),
        )
        rows = self.cursor.fetchall()
        print("Exercises (WorkoutExerciseId, ExerciseId, Name, Type, Sets, Reps, Weight, Duration, Distance):")
        if not rows:
            print("(no exercises for this workout)")
            return
        for row in rows:
            print(row)


def main():
    db_path = 'my_database.db'
    connection = sqlite3.connect(db_path)
    q = query(connection)

    def setup_and_populate_db():
        nonlocal connection, q

        try:
            connection.close()
        except sqlite3.Error:
            pass

        if os.path.exists(db_path):
            os.remove(db_path)

        connection = sqlite3.connect(db_path)
        cursor = connection.cursor()

        with open('3241CreateM2.txt', 'r', encoding='utf-8') as file:
            sql_script = file.read()
        cursor.executescript(sql_script)
        connection.commit()

        with open('3241PopulateM2.txt', 'r', encoding='utf-8') as file:
            sql_script = file.read()
        cursor.executescript(sql_script)
        connection.commit()

        print("\nDatabase created and populated. Users table:")
        for row in cursor.execute("SELECT * FROM User"):
            print(row)

        q = query(connection)

    def run_safely(fn):
        try:
            fn()
        except sqlite3.OperationalError as exc:
            print(f"Database error: {exc}")
            print("Run option 10 to create and populate the database.")

    while True:
        print("\nWhich query would you like to run?")
        print("0. List all workouts for a user (by UserId)")
        print("1. Users who lifted more than 100 pounds")
        print("2. Muscle groups and their exercises")
        print("3. Total distance covered by each user")
        print("4. List all exercises (Id, Name, Strength/Endurance)")
        print("5. Add a user")
        print("6. Add a workout")
        print("7. Add an exercise to a workout")
        print("8. Get a specific workout's information")
        print("9. Exit")
        print("10. Create and populate the database")

        choice = input("Enter your choice: ")

        if choice == "0":
            print("\nQuery 5: Workouts for a specific user:")
            run_safely(q.execute_query_five)

        elif choice == "1":
            print("\nQuery 1: Users who lifted more than 100 pounds:")
            run_safely(q.execute_query_one)

        elif choice == "2":
            print("\nQuery 2: Muscle groups and their exercises:")
            run_safely(q.execute_query_two)

        elif choice == "3":
            print("\nQuery 3: Total distance covered by each user:")
            run_safely(q.execute_query_three)

        elif choice == "4":
            print("\nQuery 4: Exercises (Id, Name, Strength/Endurance):")
            run_safely(q.execute_query_four)

        elif choice == "5":
            run_safely(q.add_user)

        elif choice == "6":
            run_safely(q.add_workout)

        elif choice == "7":
            run_safely(q.add_exercise_to_workout)

        elif choice == "8":
            run_safely(q.get_workout_info)

        elif choice == "9":
            print("Exiting program.")
            break

        elif choice == "10":
            setup_and_populate_db()

        else:
            print("Invalid choice. Please enter 0-10.")

    connection.close()


if __name__ == "__main__":
    main()
