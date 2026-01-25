"""
Model training for Calorie Tracker.
Trains Linear Regression (baseline) and Random Forest; picks the best by R²
and saves a single sklearn Pipeline (preprocessor + model) as model.pkl.
"""
import os
import pandas as pd
import joblib
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score

ML_DIR = os.path.dirname(__file__)
DATA_PATH = os.path.join(ML_DIR, "data", "calorie_data.csv")
MODEL_PATH = os.path.join(ML_DIR, "model.pkl")

RANDOM_STATE = 42
TEST_SIZE = 0.2

FEATURE_COLS = ["age", "gender", "height", "weight", "activity", "goal"]
TARGET_COL = "calorie_target"
NUM_COLS = ["age", "height", "weight"]
CAT_COLS = ["gender", "activity", "goal"]


def build_pipeline(model):
    preprocessor = ColumnTransformer(
        [
            ("num", StandardScaler(), NUM_COLS),
            (
                "cat",
                OneHotEncoder(drop="first", handle_unknown="ignore", sparse_output=False),
                CAT_COLS,
            ),
        ]
    )
    return Pipeline(steps=[("preprocessor", preprocessor), ("model", model)])


def load_data():
    if not os.path.isfile(DATA_PATH):
        raise FileNotFoundError(
            f"Dataset not found: {DATA_PATH}. Run: python ml/dataset_generator.py"
        )
    df = pd.read_csv(DATA_PATH)
    X = df[FEATURE_COLS]
    y = df[TARGET_COL]
    return X, y


def evaluate(y_true, y_pred, name):
    mse = mean_squared_error(y_true, y_pred)
    mae = mean_absolute_error(y_true, y_pred)
    r2 = r2_score(y_true, y_pred)
    print(f"  {name}: MSE={mse:.2f}, MAE={mae:.2f}, R2={r2:.4f}")
    return mse, mae, r2


def main():
    X, y = load_data()
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=TEST_SIZE, random_state=RANDOM_STATE
    )

    pipe_lr = build_pipeline(LinearRegression())
    pipe_rf = build_pipeline(
        RandomForestRegressor(
            n_estimators=150,
            max_depth=12,
            min_samples_leaf=4,
            random_state=RANDOM_STATE,
        )
    )

    print("Training Linear Regression (baseline)...")
    pipe_lr.fit(X_train, y_train)
    print("Training Random Forest...")
    pipe_rf.fit(X_train, y_train)

    print("\nTest set performance:")
    _, _, r2_lr = evaluate(y_test, pipe_lr.predict(X_test), "Linear Regression")
    _, _, r2_rf = evaluate(y_test, pipe_rf.predict(X_test), "Random Forest")

    if r2_rf >= r2_lr:
        best = pipe_rf
        name = "Random Forest"
    else:
        best = pipe_lr
        name = "Linear Regression"

    os.makedirs(ML_DIR, exist_ok=True)
    joblib.dump(best, MODEL_PATH)
    print(f"\nSaved best model ({name}) -> {MODEL_PATH}")


if __name__ == "__main__":
    main()
