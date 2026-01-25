"""
Prediction wrapper for Calorie Tracker.
Loads the trained pipeline and predicts daily calorie requirement from raw inputs.
"""
import os
import pandas as pd
import joblib

ML_DIR = os.path.dirname(__file__)
MODEL_PATH = os.path.join(ML_DIR, "model.pkl")

FEATURE_COLS = ["age", "gender", "height", "weight", "activity", "goal"]


def predict_calories(age: int, gender: str, height: float, weight: float, activity: str, goal: str):
    """
    Predict daily calorie target (kcal) from user inputs.
    Returns a float or None if the model file is missing.
    """
    if not os.path.isfile(MODEL_PATH):
        return None
    try:
        pipeline = joblib.load(MODEL_PATH)
        X = pd.DataFrame(
            [{"age": age, "gender": gender, "height": height, "weight": weight, "activity": activity, "goal": goal}],
            columns=FEATURE_COLS,
        )
        pred = pipeline.predict(X)[0]
        return round(float(pred), 2)
    except Exception:
        return None
