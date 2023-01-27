#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import datetime
import enum

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class UserRole(enum.IntEnum):
    SAdimn = 1
    Admin = 2
    User = 3


class ExerciseType(enum.IntEnum):
    GapTextExercise = 1
    SyntaxExercise = 2
    ParsonsPuzzleExercise = 3
    FindTheBugExercise = 4
    DocumentationExercise = 5
    OutputExercise = 6
    ProgrammingExercise = 7


class ExerciseLanguage(enum.IntEnum):
    Python = 1
    Java = 2


class UserModel(db.Model):
    user_id = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.String, nullable=False)
    user_pass = db.Column(db.String(64), nullable=False)
    user_mail = db.Column(db.String, nullable=False, unique=True)
    user_role = db.Column(db.Enum(UserRole), nullable=False)

    def __init__(
        self, user_name: str, user_pass: str, user_mail: str, user_role: UserRole | int
    ) -> None:
        self.user_name = user_name
        self.user_pass = user_pass
        self.user_mail = user_mail
        self.user_role = (
            user_role if isinstance(user_role, UserRole) else UserRole(user_role)
        )

    def __repr__(self) -> str:
        return f"yUser id={self.user_id} name={self.user_name} mail={self.user_mail}, role={self.user_role}"


class ExerciseModel(db.Model):
    exercise_id = db.Column(db.Integer, primary_key=True)
    exercise_title = db.Column(db.String, nullable=False, unique=True)
    exercise_description = db.Column(db.String)
    exercise_type = db.Column(db.Enum(ExerciseType), nullable=False)
    exercise_content = db.Column(db.Text)
    exercise_solution = db.Column(db.Text)
    exercise_language = db.Column(db.Enum(ExerciseLanguage), nullable=False)

    def __init__(
        self,
        exercise_title: str,
        exercise_description: str,
        exercise_type: ExerciseType | int,
        exercise_content: str,
        exercise_solution: str,
        exercise_language: ExerciseLanguage | int,
    ) -> None:
        self.exercise_title = exercise_title
        self.exercise_description = exercise_description
        self.exercise_type = (
            exercise_type
            if isinstance(exercise_type, ExerciseType)
            else ExerciseType(exercise_type)
        )
        self.exercise_content = exercise_content
        self.exercise_solution = exercise_solution
        self.exercise_language = (
            exercise_language
            if isinstance(exercise_language, ExerciseLanguage)
            else ExerciseLanguage(exercise_language)
        )

    def __repr__(self) -> str:
        return f"<Exercise id={self.exercise_id} title={self.exercise_title} type={self.exercise_type} language={self.exercise_language}>"


class SolutionModel(db.Model):
    solution_id = db.Column(db.Integer, primary_key=True)
    solution_user = db.Column(
        db.Integer, db.ForeignKey(UserModel.user_id), nullable=False
    )
    solution_exercise = db.Column(
        db.Integer, db.ForeignKey(ExerciseModel.exercise_id), nullable=False
    )
    solution_date = db.Column(db.DateTime)
    solution_duration = db.Column(db.Interval)
    solution_correct = db.Column(db.Boolean)
    solution_pending = db.Column(db.Boolean)
    solution_content = db.Column(db.Text)

    def __init__(
        self,
        solution_user: int,
        solution_exercise: int,
        solution_date: datetime.datetime | int,
        solution_duration: datetime.timedelta | int,
        solution_correct: bool,
        solution_pending: bool,
        solution_content: str,
    ) -> None:
        self.solution_user = solution_user
        self.solution_exercise = solution_exercise
        self.solution_date = (
            solution_date
            if isinstance(solution_date, datetime.datetime)
            else datetime.datetime.fromtimestamp(solution_date)
        )
        self.solution_duration = (
            solution_duration
            if isinstance(solution_duration, datetime.timedelta)
            else datetime.timedelta(seconds=solution_duration)
        )
        self.solution_correct = solution_correct
        self.solution_pending = solution_pending
        self.solution_content = solution_content