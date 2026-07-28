from flask import Flask, request
from flask_migrate import Migrate
from marshmallow import ValidationError


from models import db, Exercise, Workout, WorkoutExercise
from schemas import ExerciseSchema, WorkoutSchema, WorkoutExerciseSchema

from models import db

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///app.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)
migrate = Migrate(app, db)

@app.route("/workouts", methods=["GET"])
def get_workouts():
    workouts = Workout.query.all()
    schema = WorkoutSchema(many=True)

    return schema.dump(workouts), 200


@app.route("/workouts/<int:id>", methods=["GET"])
def get_workout(id):
    workout = db.session.get(Workout, id)

    if not workout:
        return {"error": "Workout not found"}, 404

    schema = WorkoutSchema()

    return schema.dump(workout), 200

@app.route("/workouts", methods=["POST"])
def create_workout():
    data = request.get_json() or {}

    try:
        validated_data = WorkoutSchema().load(data)

        workout = Workout(**validated_data)

        db.session.add(workout)
        db.session.commit()

        return WorkoutSchema().dump(workout), 201

    except ValidationError as err:
        return {"errors": err.messages}, 400

@app.route("/workouts/<int:id>", methods=["DELETE"])
def delete_workout(id):
    workout = db.session.get(Workout, id)

    if not workout:
        return {"error": "Workout not found"}, 404

    db.session.delete(workout)
    db.session.commit()

    return {"message": "Workout deleted successfully"}, 200

@app.route("/exercises", methods=["GET"])
def get_exercises():
    exercises = Exercise.query.all()

    schema = ExerciseSchema(many=True)

    return schema.dump(exercises), 200

@app.route("/exercises/<int:id>", methods=["GET"])
def get_exercise(id):
    exercise = db.session.get(Exercise, id)

    if not exercise:
        return {"error": "Exercise not found"}, 404

    schema = ExerciseSchema()

    return schema.dump(exercise), 200

@app.route("/exercises", methods=["POST"])
def create_exercise():
    data = request.get_json()

    schema = ExerciseSchema()

    try:
        exercise_data = schema.load(data)
    except Exception as e:
        return {"errors": str(e)}, 400

    exercise = Exercise(**exercise_data)

    db.session.add(exercise)
    db.session.commit()

    return schema.dump(exercise), 201

@app.route("/exercises/<int:id>", methods=["DELETE"])
def delete_exercise(id):
    exercise = db.session.get(Exercise, id)

    if not exercise:
        return {"error": "Exercise not found"}, 404

    db.session.delete(exercise)
    db.session.commit()

    return {"message": "Exercise deleted successfully"}, 200


@app.route(
    "/workouts/<int:workout_id>/exercises/<int:exercise_id>/workout_exercises",
    methods=["POST"]
)
def add_exercise_to_workout(workout_id, exercise_id):
    workout = db.session.get(Workout, workout_id)
    exercise = db.session.get(Exercise, exercise_id)

    if not workout:
        return {"error": "Workout not found"}, 404

    if not exercise:
        return {"error": "Exercise not found"}, 404

    existing = WorkoutExercise.query.filter_by(
        workout_id=workout_id,
        exercise_id=exercise_id
    ).first()

    if existing:
        return {
            "error": "Exercise is already added to this workout"
        }, 400

    data = request.get_json() or {}

    schema = WorkoutExerciseSchema()

    try:
        workout_exercise_data = schema.load({
            "workout_id": workout_id,
            "exercise_id": exercise_id,
            "reps": data.get("reps"),
            "sets": data.get("sets"),
            "duration_seconds": data.get("duration_seconds")
        })
    except Exception as e:
        return {"errors": str(e)}, 400

    workout_exercise = WorkoutExercise(
        **workout_exercise_data
    )

    db.session.add(workout_exercise)
    db.session.commit()

    return schema.dump(workout_exercise), 201

if __name__ == "__main__":
    app.run(port=5555, debug=True)
