"""
Database helper functions for Calorie Tracker.
Provides convenient functions for database operations.
"""
import sqlite3
from database.init_db import get_db_connection


def get_user_by_username(username):
    """Get user by username."""
    conn = get_db_connection()
    user = conn.execute(
        "SELECT * FROM users WHERE username = ?", (username,)
    ).fetchone()
    conn.close()
    return user


def get_user_by_email(email):
    """Get user by email."""
    conn = get_db_connection()
    user = conn.execute(
        "SELECT * FROM users WHERE email = ?", (email,)
    ).fetchone()
    conn.close()
    return user


def create_user(username, email, password_hash):
    """Create a new user."""
    conn = get_db_connection()
    try:
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO users (username, email, password_hash) VALUES (?, ?, ?)",
            (username, email, password_hash)
        )
        conn.commit()
        user_id = cursor.lastrowid
        conn.close()
        return user_id
    except sqlite3.IntegrityError:
        conn.close()
        return None


def save_user_data(user_id, age, gender, height, weight, activity_level, goal):
    """Save user input data."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        """INSERT INTO user_data 
           (user_id, age, gender, height, weight, activity_level, goal) 
           VALUES (?, ?, ?, ?, ?, ?, ?)""",
        (user_id, age, gender, height, weight, activity_level, goal)
    )
    conn.commit()
    data_id = cursor.lastrowid
    conn.close()
    return data_id


def save_prediction(user_id, bmr, tdee, calorie_target, ml_prediction,
                   protein, carbs, fats, exercise_type=None, exercise_duration=None):
    """Save prediction results."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        """INSERT INTO predictions 
           (user_id, bmr, tdee, calorie_target, ml_prediction, 
            protein, carbs, fats, exercise_type, exercise_duration) 
           VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
        (user_id, bmr, tdee, calorie_target, ml_prediction,
         protein, carbs, fats, exercise_type, exercise_duration)
    )
    conn.commit()
    pred_id = cursor.lastrowid
    conn.close()
    return pred_id


def get_user_predictions(user_id, limit=10):
    """Get recent predictions for a user."""
    conn = get_db_connection()
    predictions = conn.execute(
        """SELECT * FROM predictions 
           WHERE user_id = ? 
           ORDER BY created_at DESC 
           LIMIT ?""",
        (user_id, limit)
    ).fetchall()
    conn.close()
    return predictions


def get_user_data_history(user_id, limit=10):
    """Get recent user data entries."""
    conn = get_db_connection()
    history = conn.execute(
        """SELECT * FROM user_data 
           WHERE user_id = ? 
           ORDER BY created_at DESC 
           LIMIT ?""",
        (user_id, limit)
    ).fetchall()
    conn.close()
    return history
