#!/usr/bin/env python3

from datetime import date

from app import app
from models import db, Exercise, Workout, WorkoutExercise


with app.app_context():

    print("Clearing existing data...")

    WorkoutExercise.query.delete()
    Workout.query.delete()
    Exercise.query.delete()

    db.session.commit()

    print("Creating exercises...")

    bench_press = Exercise(
        name="Bench Press",
        category="Strength",
        equipment_needed=True
    )

    squats = Exercise(
        name="Squats",
        category="Strength",
        equipment_needed=True
    )

    running = Exercise(
        name="Running",
        category="Cardio",
        equipment_needed=False
    )

    push_ups = Exercise(
        name="Push Ups",
        category="Bodyweight",
        equipment_needed=False
    )

    db.session.add_all([
        bench_press,
        squats,
        running,
        push_ups
    ])

    db.session.commit()

    print("Creating workouts...")

    workout_1 = Workout(
        date=date(2026, 7, 27),
        duration_minutes=60,
        notes="Upper body strength workout"
    )

    workout_2 = Workout(
        date=date(2026, 7, 28),
        duration_minutes=45,
        notes="Lower body strength workout"
    )

    workout_3 = Workout(
        date=date(2026, 7, 29),
        duration_minutes=30,
        notes="Cardio workout"
    )

    db.session.add_all([
        workout_1,
        workout_2,
        workout_3
    ])

    db.session.commit()

    print("Adding exercises to workouts...")

    workout_exercise_1 = WorkoutExercise(
        workout=workout_1,
        exercise=bench_press,
        reps=10,
        sets=3,
        duration_seconds=None
    )

    workout_exercise_2 = WorkoutExercise(
        workout=workout_1,
        exercise=push_ups,
        reps=15,
        sets=3,
        duration_seconds=None
    )

    workout_exercise_3 = WorkoutExercise(
        workout=workout_2,
        exercise=squats,
        reps=12,
        sets=4,
        duration_seconds=None
    )

    workout_exercise_4 = WorkoutExercise(
        workout=workout_3,
        exercise=running,
        reps=None,
        sets=None,
        duration_seconds=1800
    )

    db.session.add_all([
        workout_exercise_1,
        workout_exercise_2,
        workout_exercise_3,
        workout_exercise_4
    ])

    db.session.commit()

    print("Database seeded successfully!")
