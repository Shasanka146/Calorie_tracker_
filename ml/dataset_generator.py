"""
Synthetic dataset generator for Calorie Tracker.
Generates 10,000 samples using the same BMR (Mifflin-St Jeor) and TDEE
formulas as the app, with realistic distributions and controlled noise.
"""
import os
import numpy as np
import pandas as pd

# Output path
ML_DIR = os.path.dirname(__file__)
DATA_DIR = os.path.join(ML_DIR, "data")
DATA_PATH = os.path.join(DATA_DIR, "calorie_data.csv")

# Reproducibility
RANDOM_STATE = 42
np.random.seed(RANDOM_STATE)

# Same formulas as app.py (Mifflin-St Jeor)
ACTIVITY_MAP = {"sedentary": 1.2, "light": 1.375, "moderate": 1.55, "active": 1.725}
GOAL_MAP = {"loss": -500, "maintain": 0, "gain": 500}

N_SAMPLES = 10_000
NOISE_STD = 0.07  # ~7% variation to simulate individual differences
CAL_MIN, CAL_MAX = 800, 5500


def _bmr(age: float, gender: str, height: float, weight: float) -> float:
    """Mifflin-St Jeor BMR (kcal/day)."""
    base = (10 * weight) + (6.25 * height) - (5 * age)
    return base + 5 if gender == "male" else base - 161


def _tdee(bmr: float, activity: str) -> float:
    return bmr * ACTIVITY_MAP.get(activity, 1.2)


def _calorie_target(tdee: float, goal: str) -> float:
    return tdee + GOAL_MAP.get(goal, 0)


def _add_noise(value: float) -> float:
    return value * (1 + np.random.normal(0, NOISE_STD))


def generate_dataset(n: int = N_SAMPLES) -> pd.DataFrame:
    """Generate n samples with realistic feature distributions."""
    ages = np.clip(np.random.normal(40, 18, n).astype(int), 15, 100)
    genders = np.random.choice(["male", "female"], size=n)

    heights = np.zeros(n)
    for i in range(n):
        if genders[i] == "male":
            heights[i] = np.clip(np.random.normal(175, 9), 150, 210)
        else:
            heights[i] = np.clip(np.random.normal(162, 8), 140, 200)

    # Weight from BMI for realism (BMI 16–40)
    bmis = np.clip(np.random.normal(24, 4.5, n), 16, 40)
    weights = (heights / 100) ** 2 * bmis
    weights = np.clip(weights, 35, 180)

    activities = np.random.choice(
        ["sedentary", "light", "moderate", "active"],
        size=n,
        p=[0.28, 0.32, 0.26, 0.14],
    )
    goals = np.random.choice(
        ["loss", "maintain", "gain"],
        size=n,
        p=[0.35, 0.35, 0.30],
    )

    targets = []
    for i in range(n):
        bmr = _bmr(ages[i], genders[i], heights[i], weights[i])
        tdee = _tdee(bmr, activities[i])
        cal = _calorie_target(tdee, goals[i])
        cal = _add_noise(cal)
        cal = np.clip(cal, CAL_MIN, CAL_MAX)
        targets.append(round(cal, 2))

    df = pd.DataFrame({
        "age": ages,
        "gender": genders,
        "height": np.round(heights, 1),
        "weight": np.round(weights, 1),
        "activity": activities,
        "goal": goals,
        "calorie_target": targets,
    })
    return df


def main():
    os.makedirs(DATA_DIR, exist_ok=True)
    df = generate_dataset(N_SAMPLES)
    df.to_csv(DATA_PATH, index=False)
    print(f"Generated {len(df)} samples -> {DATA_PATH}")
    print(df.describe())


if __name__ == "__main__":
    main()
