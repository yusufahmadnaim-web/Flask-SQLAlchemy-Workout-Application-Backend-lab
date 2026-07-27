# Flask SQLAlchemy Workout Application Backend

## Project Description

This project is a backend API for a workout tracking application designed for personal trainers. The API allows trainers to create, view, and delete workouts and exercises, as well as add reusable exercises to workouts.

Each workout can contain multiple exercises. The application uses a join table called `WorkoutExercise` to associate workouts with exercises and store additional information about each exercise within a workout, including the number of sets, repetitions, and duration.

The API is built using Flask, Flask-SQLAlchemy, Flask-Migrate, and Marshmallow. It includes database relationships, table constraints, model validations, schema validations, serialization, deserialization, and RESTful API endpoints.

## Technologies Used

* Python 3.8+
* Flask 2.2.2
* Flask-SQLAlchemy 3.0.3
* Flask-Migrate 3.1.0
* Marshmallow 3.20.1
* SQLite
* Pipenv

## Installation Instructions

### 1. Clone the repository

```bash
git clone <your-github-repository-url>
cd Flask-SQLAlchemy-Workout-Application-Backend-lab
```

### 2. Install dependencies

Install the required Python packages using Pipenv:

```bash
pipenv install
```

### 3. Activate the virtual environment

```bash
pipenv shell
```

### 4. Navigate to the server directory

```bash
cd server
```

### 5. Initialize the database migrations

If the migrations folder does not already exist, run:

```bash
flask db init
```

### 6. Create a database migration

After creating or changing the SQLAlchemy models, run:

```bash
flask db migrate -m "Create workout application database models"
```

### 7. Apply the migration

```bash
flask db upgrade head
```

### 8. Seed the database

Populate the database with sample exercises, workouts, and workout-exercise relationships:

```bash
python seed.py
```

The seed file can be run again to reset the database and recreate the sample data without duplicating records.

## Run Instructions

From the `server` directory, start the Flask application with:

```bash
flask run --port 5555
```

Alternatively, you can run:

```bash
python app.py
```

The API will be available at:

```text
http://127.0.0.1:5555
```

## API Endpoints

### Workouts

#### GET `/workouts`

Returns a list of all workouts.

---

#### GET `/workouts/<id>`

Returns a single workout by ID and includes its associated exercises.

Where applicable, the response includes exercise-specific information such as:

* Repetitions
* Sets
* Duration in seconds

---

#### POST `/workouts`

Creates a new workout.

Example request body:

```json
{
  "date": "2026-07-27",
  "duration_minutes": 60,
  "notes": "Full body strength workout"
}
```

---

#### DELETE `/workouts/<id>`

Deletes a workout by ID.

Associated `WorkoutExercise` records are also deleted where applicable.

---

### Exercises

#### GET `/exercises`

Returns a list of all exercises.

---

#### GET `/exercises/<id>`

Returns a single exercise by ID and its associated workouts.

---

#### POST `/exercises`

Creates a new exercise.

Example request body:

```json
{
  "name": "Bench Press",
  "category": "Strength",
  "equipment_needed": true
}
```

---

#### DELETE `/exercises/<id>`

Deletes an exercise by ID.

Associated `WorkoutExercise` records are also deleted where applicable.

---

### Workout Exercises

#### POST `/workouts/<workout_id>/exercises/<exercise_id>/workout_exercises`

Adds an existing exercise to an existing workout.

The endpoint accepts exercise-specific information such as repetitions, sets, and duration.

Example request:

```text
POST /workouts/1/exercises/1/workout_exercises
```

Example request body:

```json
{
  "reps": 10,
  "sets": 3,
  "duration_seconds": 60
}
```

## Database Models

### Exercise

Represents a reusable exercise.

Fields:

* `id` — Integer primary key
* `name` — Exercise name
* `category` — Exercise category
* `equipment_needed` — Boolean indicating whether equipment is required

### Workout

Represents a workout session.

Fields:

* `id` — Integer primary key
* `date` — Date of the workout
* `duration_minutes` — Duration of the workout in minutes
* `notes` — Additional workout notes

### WorkoutExercise

Join table connecting workouts and exercises.

Fields:

* `id` — Integer primary key
* `workout_id` — Foreign key referencing a workout
* `exercise_id` — Foreign key referencing an exercise
* `reps` — Number of repetitions
* `sets` — Number of sets
* `duration_seconds` — Exercise duration in seconds

## Relationships

* A `WorkoutExercise` belongs to a `Workout`.
* A `WorkoutExercise` belongs to an `Exercise`.
* A `Workout` has many `WorkoutExercises`.
* An `Exercise` has many `WorkoutExercises`.
* A `Workout` has many `Exercises` through `WorkoutExercises`.
* An `Exercise` has many `Workouts` through `WorkoutExercises`.

## Validations and Constraints

The application implements validations at multiple levels to ensure data integrity.

### Table Constraints

The database uses constraints to prevent invalid or duplicate data.

### Model Validations

SQLAlchemy model-level validations ensure that invalid data is rejected before it is saved to the database.

### Schema Validations

Marshmallow schemas validate incoming API data before it is deserialized and stored.

The application includes more than one validation at each required level.

## Git Commit Guidelines

Meaningful Git commits are used throughout the project to track development progress.

Examples:

```bash
git add .
git commit -m "Add Exercise model and validations"
```

```bash
git add .
git commit -m "Add Workout model and relationships"
```

```bash
git add .
git commit -m "Add WorkoutExercise join model"
```

```bash
git add .
git commit -m "Add Marshmallow schemas and validations"
```

```bash
git add .
git commit -m "Implement workout API endpoints"
```

## Project Structure

```text
Flask-SQLAlchemy-Workout-Application-Backend-lab/
├── README.md
├── .gitignore
├── Pipfile
├── Pipfile.lock
└── server/
    ├── app.py
    ├── models.py
    ├── schemas.py
    ├── seed.py
    ├── migrations/
    └── instance/
```

