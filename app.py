from flask import Flask, render_template, request, redirect, url_for, session, flash
from database.init_db import init_database, get_db_connection
from database.db_helper import (
    save_user_data, save_prediction, get_user_predictions, get_user_data_history
)
from auth.login import authenticate_user
from auth.register import register_user
from ml.predict import predict_calories
from core.exercise import recommend
import os

app = Flask(__name__)
# For a real project, load this from environment (e.g. using python-dotenv)
app.secret_key = "change-this-secret-key"

# Initialize database on startup
DB_DIR = os.path.join(os.path.dirname(__file__), "database")
if not os.path.exists(DB_DIR):
    os.makedirs(DB_DIR)
init_database()


@app.route("/")
def index():
    """Landing page."""
    if session.get("user"):
        return redirect(url_for("dashboard"))
    return render_template("index.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    """User registration page."""
    if session.get("user"):
        return redirect(url_for("dashboard"))
    
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        email = request.form.get("email", "").strip()
        password = request.form.get("password", "")
        confirm_password = request.form.get("confirm_password", "")
        
        # Check if passwords match
        if password != confirm_password:
            flash("Passwords do not match.", "error")
            return redirect(url_for("register"))
        
        # Register user
        success, message, user_id = register_user(username, email, password)
        
        if success:
            flash(message, "success")
            return redirect(url_for("login"))
        else:
            flash(message, "error")
            return redirect(url_for("register"))
    
    return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    """User login page with password authentication."""
    if session.get("user"):
        return redirect(url_for("dashboard"))
    
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "")
        
        # Authenticate user
        success, message, user = authenticate_user(username, password)
        
        if success:
            session["user"] = user["username"]
            session["user_id"] = user["id"]
            flash(message, "success")
            return redirect(url_for("dashboard"))
        else:
            flash(message, "error")
            return redirect(url_for("login"))
    
    return render_template("login.html")


@app.route("/history")
def history():
    """View user's calculation history."""
    if not session.get("user"):
        return redirect(url_for("login"))
    
    user_id = session.get("user_id")
    predictions = get_user_predictions(user_id, limit=20)
    
    # Convert Row objects to dictionaries for template
    history_data = []
    for pred in predictions:
        history_data.append({
            "id": pred["id"],
            "bmr": pred["bmr"],
            "tdee": pred["tdee"],
            "calorie_target": pred["calorie_target"],
            "ml_prediction": pred["ml_prediction"],
            "protein": pred["protein"],
            "carbs": pred["carbs"],
            "fats": pred["fats"],
            "exercise_type": pred["exercise_type"],
            "exercise_duration": pred["exercise_duration"],
            "created_at": pred["created_at"],
        })
    
    return render_template("history.html", user=session.get("user"), history=history_data)


@app.route("/logout")
def logout():
    """Clear session and return to home."""
    session.clear()
    flash("Logged out successfully.", "info")
    return redirect(url_for("index"))


@app.route("/dashboard", methods=["GET", "POST"])
def dashboard():
    """Main calorie calculator page."""
    if not session.get("user"):
        return redirect(url_for("login"))
    
    user_id = session.get("user_id")
    result = None

    if request.method == "POST":
        try:
            age = int(request.form.get("age", 0))
            gender = request.form.get("gender")
            height = float(request.form.get("height", 0.0))  # cm
            weight = float(request.form.get("weight", 0.0))  # kg
            activity = request.form.get("activity")
            goal = request.form.get("goal")
        except ValueError:
            flash("Please enter valid numeric values.", "error")
            return redirect(url_for("dashboard"))

        # --- BMR: Mifflin-St Jeor ---
        if gender == "male":
            bmr = (10 * weight) + (6.25 * height) - (5 * age) + 5
        else:
            bmr = (10 * weight) + (6.25 * height) - (5 * age) - 161

        # --- Activity multipliers ---
        activity_map = {
            "sedentary": 1.2,
            "light": 1.375,
            "moderate": 1.55,
            "active": 1.725,
        }
        tdee = bmr * activity_map.get(activity, 1.2)

        # --- Goal adjustment ---
        if goal == "loss":
            calorie_target = tdee - 500
        elif goal == "gain":
            calorie_target = tdee + 500
        else:
            calorie_target = tdee

        # --- Macro distribution (simple demo rules) ---
        if goal == "loss":
            p_ratio, c_ratio, f_ratio = 0.30, 0.40, 0.30
        elif goal == "gain":
            p_ratio, c_ratio, f_ratio = 0.25, 0.50, 0.25
        else:
            p_ratio, c_ratio, f_ratio = 0.25, 0.45, 0.30

        protein_cal = calorie_target * p_ratio
        carb_cal = calorie_target * c_ratio
        fat_cal = calorie_target * f_ratio

        # Convert kcal to grams (protein & carbs: 4 kcal/g, fats: 9 kcal/g)
        protein_g = protein_cal / 4
        carbs_g = carb_cal / 4
        fats_g = fat_cal / 9

        ml_pred = predict_calories(age, gender, height, weight, activity, goal)
        ex = recommend(goal, activity)
        result = {
            "bmr": round(bmr, 2),
            "tdee": round(tdee, 2),
            "calorie_target": round(calorie_target, 2),
            "protein_g": round(protein_g, 1),
            "carbs_g": round(carbs_g, 1),
            "fats_g": round(fats_g, 1),
            "goal": goal,
            "ml_prediction": ml_pred,
            "exercise_type": ex["exercise_type"],
            "exercise_duration": ex["exercise_duration"],
            "exercise_frequency": ex["exercise_frequency"],
        }

        # Save to database
        try:
            save_user_data(user_id, age, gender, height, weight, activity, goal)
            save_prediction(
                user_id=user_id,
                bmr=result["bmr"],
                tdee=result["tdee"],
                calorie_target=result["calorie_target"],
                ml_prediction=ml_pred,
                protein=result["protein_g"],
                carbs=result["carbs_g"],
                fats=result["fats_g"],
                exercise_type=ex["exercise_type"],
                exercise_duration=ex["exercise_duration"],
            )
        except Exception as e:
            # Log error but don't break the user experience
            print(f"Error saving to database: {e}")

    return render_template("dashboard.html", user=session.get("user"), result=result)


if __name__ == "__main__":
    # Debug mode is helpful during development
    app.run(debug=True)

