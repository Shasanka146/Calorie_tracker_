# 🍽️ Smart Calorie Tracker & Recommendation System

## 📌 Project Overview

The **Smart Calorie Tracker System** is an intelligent web-based application that calculates personalized daily calorie requirements using both **scientific formulas** and **machine learning predictions**. It provides comprehensive food intake suggestions and exercise recommendations tailored to individual fitness goals.

---

## ✨ Key Features

- 🔐 **Multi-user Authentication System**
- 📊 **BMR & TDEE Calculation** (Mifflin-St Jeor Formula)
- 🤖 **Machine Learning Predictions** (Random Forest Regressor)
- 🥗 **Macronutrient Breakdown** (Protein, Carbs, Fats)
- 💪 **Personalized Exercise Recommendations**
- 📈 **User History Tracking**
- 🎯 **Goal-based Calorie Adjustment** (Weight Loss/Maintain/Gain)

---

## 🎯 Input Features

The system collects the following user data:

| Feature | Type | Options |
|---------|------|---------|
| Age | Integer | 15-100 years |
| Gender | Categorical | Male / Female |
| Height | Float | cm |
| Weight | Float | kg |
| Activity Level | Categorical | Sedentary / Light / Moderate / Active |
| Fitness Goal | Categorical | Weight Loss / Maintain / Weight Gain |

---

## 📤 System Outputs

### 1. **Calorie Calculations**
- Basal Metabolic Rate (BMR)
- Total Daily Energy Expenditure (TDEE)
- Goal-adjusted calorie target
- ML-predicted calorie requirement

### 2. **Macronutrient Distribution**
- Protein (grams & percentage)
- Carbohydrates (grams & percentage)
- Fats (grams & percentage)

### 3. **Exercise Recommendations**
- Exercise type (Cardio / Strength / Mixed)
- Duration (minutes per session)
- Frequency (days per week)

### 4. **Progress Prediction**
- Estimated weekly weight change

---

## 🏗️ Project Structure

```
Calorie_Tracker/
│
├── app.py                          # Main Flask application
├── requirements.txt                # Python dependencies
├── README.md                       # Project documentation
│
├── database/
│   ├── init_db.py                 # Database initialization script
│   └── calorie_tracker.db         # SQLite database (auto-generated)
│
├── auth/
│   ├── __init__.py
│   ├── login.py                   # Login logic
│   └── register.py                # Registration logic
│
├── core/
│   ├── __init__.py
│   ├── bmr.py                     # BMR calculation
│   ├── tdee.py                    # TDEE calculation
│   ├── macros.py                  # Macronutrient distribution
│   └── exercise.py                # Exercise recommendations
│
├── ml/
│   ├── __init__.py
│   ├── dataset_generator.py      # Synthetic dataset creation
│   ├── train_model.py            # Model training script
│   ├── predict.py                # Prediction wrapper
│   └── model.pkl                 # Trained ML model (auto-generated)
│
├── templates/
│   ├── base.html                 # Base template
│   ├── login.html                # Login page
│   ├── register.html             # Registration page
│   ├── dashboard.html            # User input dashboard
│   └── result.html               # Results & recommendations
│
└── static/
    └── style.css                 # CSS styling
```

---

## 🧮 Scientific Formulas

### 1. Basal Metabolic Rate (BMR) - Mifflin-St Jeor Equation

**For Males:**
```
BMR = (10 × weight_kg) + (6.25 × height_cm) - (5 × age) + 5
```

**For Females:**
```
BMR = (10 × weight_kg) + (6.25 × height_cm) - (5 × age) - 161
```

### 2. Total Daily Energy Expenditure (TDEE)

```
TDEE = BMR × Activity_Factor
```

**Activity Multipliers:**
- Sedentary (little/no exercise): 1.2
- Light (exercise 1-3 days/week): 1.375
- Moderate (exercise 3-5 days/week): 1.55
- Active (exercise 6-7 days/week): 1.725

### 3. Goal-Based Calorie Adjustment

- **Weight Loss:** TDEE - 500 calories (lose ~0.5 kg/week)
- **Maintain Weight:** TDEE
- **Weight Gain:** TDEE + 500 calories (gain ~0.5 kg/week)

### 4. Macronutrient Distribution

**Weight Loss:**
- Protein: 30% (1.8-2.2g per kg body weight)
- Carbs: 40%
- Fats: 30%

**Maintenance:**
- Protein: 25%
- Carbs: 45%
- Fats: 30%

**Weight Gain:**
- Protein: 25%
- Carbs: 50%
- Fats: 25%

---

## 🤖 Machine Learning Pipeline

### Dataset Generation
- **Synthetic data:** 10,000 samples
- **Features:** Age, Gender, Height, Weight, Activity Level, Goal
- **Target:** Daily calorie requirement
- **Noise:** Realistic variations added

### Models Trained
1. **Linear Regression** (Baseline)
2. **Random Forest Regressor** (Primary model)

### Model Evaluation Metrics
- Mean Squared Error (MSE)
- R² Score
- Mean Absolute Error (MAE)

### Model Selection
- Best performing model saved as `model.pkl`
- Used for real-time predictions in the web app

---

## 🛠️ Tech Stack

| Component | Technology |
|-----------|------------|
| **Backend** | Flask 3.0+ |
| **Database** | SQLite3 |
| **ML Framework** | Scikit-learn |
| **Data Processing** | NumPy, Pandas |
| **Authentication** | Flask Sessions + Werkzeug |
| **Model Serialization** | Joblib |
| **Frontend** | HTML5, CSS3, Jinja2 |

---

## 📦 Installation & Setup

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)

### Step 1: Clone/Download Project
```bash
cd Calorie_Tracker
```

### Step 2: Create Virtual Environment (Recommended)
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 4: Initialize Database
```bash
python database/init_db.py
```

### Step 5: Generate Dataset & Train Model
```bash
python ml/dataset_generator.py
python ml/train_model.py
```

### Step 6: Run Application
```bash
python app.py
```

### Step 7: Access Application
Open browser and navigate to:
```
http://127.0.0.1:5000/
```

---

## 🚀 Usage Guide

### 1. Register Account
- Navigate to registration page
- Enter username, email, and password
- Submit to create account

### 2. Login
- Use credentials to log in
- Session maintained until logout

### 3. Enter Your Data
- Fill in personal information:
  - Age, Gender, Height, Weight
  - Activity level
  - Fitness goal

### 4. Get Recommendations
- System calculates:
  - BMR & TDEE
  - ML prediction
  - Calorie target
  - Macronutrient breakdown
  - Exercise plan

### 5. View History
- Past calculations stored in database
- Track progress over time

---

## 📊 Database Schema

### Users Table
```sql
CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    email TEXT UNIQUE NOT NULL,
    password_hash TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### User Data Table
```sql
CREATE TABLE user_data (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    age INTEGER,
    gender TEXT,
    height REAL,
    weight REAL,
    activity_level TEXT,
    goal TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id)
);
```

### Predictions Table
```sql
CREATE TABLE predictions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    bmr REAL,
    tdee REAL,
    calorie_target REAL,
    ml_prediction REAL,
    protein REAL,
    carbs REAL,
    fats REAL,
    exercise_type TEXT,
    exercise_duration INTEGER,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id)
);
```

---

## 🧪 Testing

Run unit tests:
```bash
python -m pytest tests/
```

Manual testing checklist:
- [ ] User registration works
- [ ] User login/logout works
- [ ] BMR calculation accurate
- [ ] TDEE calculation accurate
- [ ] ML model predictions reasonable
- [ ] Macronutrient calculations correct
- [ ] Exercise recommendations appropriate
- [ ] Database stores data correctly

---

## 🎓 For Academic Viva

### Key Points to Explain:

1. **System Architecture**
   - Multi-tier architecture (Frontend, Backend, Database, ML)
   - Request-response flow

2. **BMR/TDEE Formulas**
   - Scientific basis (Mifflin-St Jeor)
   - Why activity multipliers matter

3. **Machine Learning Workflow**
   - Dataset generation rationale
   - Model selection (why Random Forest?)
   - Train-test split
   - Model evaluation

4. **Security Considerations**
   - Password hashing (werkzeug.security)
   - Session management
   - SQL injection prevention (parameterized queries)

5. **Database Design**
   - Normalization
   - Foreign key relationships
   - Data integrity

---

## 🔮 Future Enhancements

- [ ] Progressive web app (PWA) support
- [ ] Data visualization (charts/graphs)
- [ ] Meal planning feature
- [ ] Integration with fitness trackers
- [ ] Mobile responsive design improvements
- [ ] Export reports (PDF)
- [ ] Social features (share progress)
- [ ] Nutritionist dashboard
- [ ] Multi-language support

---

## 📝 License

This project is created for academic purposes.

---

## 👨‍💻 Author

**Shasanka Acharya**  
Smart Calorie Tracker System  
Academic Mini Project

---

## 📞 Support

For issues or questions:
- Check documentation above
- Review code comments
- Test with sample data

---

## 🙏 Acknowledgments

- Mifflin-St Jeor equation for BMR calculation
- Scikit-learn for ML framework
- Flask community for web framework

---

**Last Updated:** January 2026