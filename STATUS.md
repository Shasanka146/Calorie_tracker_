# Calorie Tracker – Status & Remaining Work

**Last updated:** January 2026

---

## Overall completion: **~75%**

| Area | Status | % |
|------|--------|---|
| Auth & Database | Done | 100% |
| BMR, TDEE, Macros, Goals | Done | 100% |
| Machine Learning | Done | 100% |
| User History | Done | 100% |
| Exercise Recommendations | Not done | 0% |
| Progress Prediction | Not done | 0% |
| Macros as % (optional) | Partial | 50% |
| Code in `core/` (optional) | Not done | 0% |

---

## ✅ DONE

### 1. Authentication & Database
- [x] Register (username, email, password, hashing)
- [x] Login with password
- [x] Logout, session, `user_id`
- [x] SQLite: `users`, `user_data`, `predictions`
- [x] `database/init_db.py`, `database/db_helper.py`
- [x] `auth/register.py`, `auth/login.py`

### 2. Calorie & Macros
- [x] BMR (Mifflin–St Jeor)
- [x] TDEE (activity multipliers)
- [x] Goal-based target (loss −500, maintain, gain +500)
- [x] Macronutrient grams (protein, carbs, fats) by goal

### 3. Machine Learning
- [x] `ml/dataset_generator.py` – 10k synthetic samples
- [x] `ml/train_model.py` – LinearRegression + RandomForest, save best
- [x] `ml/predict.py` – load `model.pkl`, predict
- [x] ML prediction shown on dashboard and in history
- [x] `ml_prediction` stored in `predictions` table

**Note:** Run `python ml/dataset_generator.py` and `python ml/train_model.py` to create `ml/model.pkl`. Without it, ML prediction is skipped.

### 4. User History
- [x] `/history` page
- [x] Last 20 predictions: BMR, TDEE, target, ML, macros, date

### 5. Frontend
- [x] `base.html`, `index.html`, `login.html`, `register.html`
- [x] `dashboard.html`, `history.html`
- [x] `style.css`, nav (Home, Dashboard, History, Login/Register, Logout)

---

## ❌ NOT DONE (from README)

### 1. Exercise recommendations (high priority)
**README:** Exercise type (Cardio / Strength / Mixed), duration (minutes), frequency (days/week).

**To do:**
1. Add `core/exercise.py` (or logic in `app.py`) that returns:
   - `exercise_type`: Cardio / Strength / Mixed (from goal + activity)
   - `exercise_duration`: e.g. 20–50 min
   - `exercise_frequency`: e.g. 2–5 days/week
2. Call it in the dashboard after the calorie/macro block.
3. Pass `exercise_type`, `exercise_duration`, `exercise_frequency` into the template.
4. Show an “Exercise” section in `dashboard.html`.
5. Save `exercise_type`, `exercise_duration` in `save_prediction` (DB already has these columns).
6. (Optional) Show exercise in `history.html`.

### 2. Progress prediction (medium priority)
**README:** “Estimated weekly weight change”.

**To do:**
1. From goal:  
   - loss: ≈ −0.5 kg/week (≈ −500 kcal/day)  
   - gain: ≈ +0.5 kg/week (≈ +500 kcal/day)  
   - maintain: 0
2. Add e.g. `result["weekly_weight_change"]` and a short line in the results:  
   “Estimated: about −0.5 kg per week” (or +0.5 / maintain).

---

## ⚠️ PARTIAL / OPTIONAL

### 1. Macros as “grams & percentage”
**README:** Protein, carbs, fats in grams and %.

- **Done:** grams.
- **To do:** compute `protein_%`, `carbs_%`, `fats_%` from the same ratios used for grams and display, e.g. “Protein: 120 g (30%)”.

### 2. `core/` modularisation (optional)
**README:** `core/bmr.py`, `core/tdee.py`, `core/macros.py`, `core/exercise.py`.

- **Current:** Logic lives in `app.py`.
- **To do:**  
  - Move BMR into `core/bmr.py`.  
  - Move TDEE into `core/tdee.py`.  
  - Move macro ratios/grams into `core/macros.py`.  
  - Add `core/exercise.py` when implementing exercise.  
  - Use these from `app.py`.

### 3. `result.html`
**README:** Separate “Results & recommendations” page.

- **Current:** Results are in `dashboard.html`.
- **Optional:** Add `result.html` and redirect to it after “Calculate”, or keep everything on the dashboard.

### 4. Food intake suggestions
**README:** “Comprehensive food intake suggestions”.

- **Current:** Not implemented.
- **Optional:** e.g. sample meals or food groups to hit the calorie and macro targets; can be a later enhancement.

---

## Suggested order to finish

1. **Exercise recommendations** (core missing feature from README).
2. **Progress prediction** (one formula, one line in the UI).
3. **Macros %** (quick addition to the existing block).
4. **`core/` refactor** (if you want the structure to match the README).
5. **`result.html` / food suggestions** (only if you want to extend further).

---

## One‑line summary

**Done:** Auth, DB, BMR/TDEE/calories, macros (g), ML, history.  
**Next:** Exercise (type, duration, frequency), then progress prediction and, if you want, macros % and `core/` refactor.
