# Databases_Project

## How to run

First, `cd` into the project directory and run the project. Before running other queries, run the `10. Create and Populate the database` query to create a sqlite database using the `3241CreateM2.txt` and `3241PopulateM2.txt` files.

Then, select any of the other queries you want to run and put in the requested inputs for each query.

When running queries that add to the database, the program will return the row(s) added to be used in other queries. For example, after you create a user, you may want to add exercises for that user.

To add exercises to an workout, first run the `4. List all exercises (Id, Name, Strength/Endurance)` query to find the Id of the exercise you want to add. Then, run the `7. Add an exercise to a workout` with the `WorkoutId` and the `ExerciseId`, along with information for the exercise.
