# ML Pipeline – Calorie Tracker

## Overview

- **Dataset:** 10,000 synthetic samples built from the same BMR (Mifflin–St Jeor) and TDEE logic as the app, with realistic distributions and ~7% noise.
- **Models:** Linear Regression (baseline) and Random Forest; the one with the better R² on the test set is saved.
- **Output:** `model.pkl` – a scikit-learn `Pipeline` (preprocessor + model) used by `predict.py` and the Flask app.

## Run order (from project root)

Ensure dependencies are installed: `pip install -r requirements.txt`

```bash
# 1. Generate data -> ml/data/calorie_data.csv
python ml/dataset_generator.py

# 2. Train and save best model -> ml/model.pkl
python ml/train_model.py
```

Then start the app: `python app.py`. If `model.pkl` is missing, the app still runs; the ML prediction is omitted.

## Files

| File | Role |
|------|------|
| `dataset_generator.py` | Builds 10k rows: age, gender, height, weight, activity, goal → calorie_target |
| `train_model.py` | Train LR and RF, compare MSE/MAE/R², save best as `model.pkl` |
| `predict.py` | Load `model.pkl`, predict from raw inputs (used by `app.py`) |
| `data/calorie_data.csv` | Generated dataset (create by running `dataset_generator.py`) |
| `model.pkl` | Trained pipeline (create by running `train_model.py`) |
