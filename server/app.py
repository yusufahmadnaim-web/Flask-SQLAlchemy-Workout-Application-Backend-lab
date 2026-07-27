from flask import Flask, make_response
from flask_migrate import Migrate

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
    return {"message": "List all workouts"}


@app.route("/workouts/<int:id>", methods=["GET"])
def get_workout(id):
    workout = db.session.get(Workout, id)

    if not workout:
        return {"error": "Workout not found"}, 404

    schema = WorkoutSchema()

    return schema.dump(workout), 200

@app.route("/workouts", methods=["POST"])
def create_workout():
    return {"message": "Create workout"}


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
    return {"message": f"Show exercise {id}"}


@app.route("/exercises", methods=["POST"])
def create_exercise():
    return {"message": "Create exercise"}


@app.route("/exercises/<int:id>", methods=["DELETE"])
def delete_exercise(id):
    return {"message": f"Delete exercise {id}"}


@app.route(
    "/workouts/<int:workout_id>/exercises/<int:exercise_id>/workout_exercises",
    methods=["POST"]
)
def add_exercise_to_workout(workout_id, exercise_id):
    return {
        "message": (
            f"Add exercise {exercise_id} "
            f"to workout {workout_id}"
        )
    }


if __name__ == "__main__":
    app.run(port=5555, debug=True)
