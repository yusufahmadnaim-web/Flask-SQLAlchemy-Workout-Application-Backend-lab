from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import validates
from sqlalchemy import CheckConstraint

db = SQLAlchemy()


class Exercise(db.Model):
    __tablename__ = "exercises"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False, unique=True)
    category = db.Column(db.String, nullable=False)
    equipment_needed = db.Column(db.Boolean, nullable=False, default=False)

    @validates("name")
    def validate_name(self, key, name):
        if not name or not name.strip():
            raise ValueError("Exercise name cannot be empty.")

        if len(name.strip()) < 2:
            raise ValueError("Exercise name must be at least 2 characters.")

        return name.strip()

    @validates("category")
    def validate_category(self, key, category):
        if not category or not category.strip():
            raise ValueError("Exercise category cannot be empty.")

        return category.strip()


class Workout(db.Model):
    __tablename__ = "workouts"

    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, nullable=False)
    duration_minutes = db.Column(db.Integer, nullable=False)
    notes = db.Column(db.Text)

    __table_args__ = (
        CheckConstraint(
            "duration_minutes > 0",
            name="check_workout_duration_positive"
        ),
    )

    @validates("duration_minutes")
    def validate_duration_minutes(self, key, duration_minutes):
        if duration_minutes <= 0:
            raise ValueError("Workout duration must be greater than 0.")

        return duration_minutes

    @validates("notes")
    def validate_notes(self, key, notes):
        if notes is not None and len(notes.strip()) > 500:
            raise ValueError("Workout notes cannot exceed 500 characters.")

        return notes