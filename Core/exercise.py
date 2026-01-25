"""
Exercise recommendations for Calorie Tracker.
Returns type (Cardio / Strength / Mixed), duration (min), and frequency (days/week)
based on goal and activity level.
"""


def recommend(goal: str, activity: str) -> dict:
    """
    Recommend exercise type, duration (minutes per session), and frequency (days/week).
    goal: 'loss' | 'maintain' | 'gain'
    activity: 'sedentary' | 'light' | 'moderate' | 'active'
    Returns: {'exercise_type': str, 'exercise_duration': int, 'exercise_frequency': int}
    """
    # --- Type: Cardio / Strength / Mixed ---
    if goal == "loss":
        if activity in ("sedentary", "light"):
            exercise_type = "Cardio"  # Emphasize fat burn
        else:
            exercise_type = "Mixed"
    elif goal == "maintain":
        exercise_type = "Mixed"
    else:  # gain
        if activity in ("moderate", "active"):
            exercise_type = "Mixed"
        else:
            exercise_type = "Strength"  # Build muscle

    # --- Duration (minutes per session) ---
    # Less active → longer sessions; more active → shorter (they already move)
    if activity == "sedentary":
        duration = 40
    elif activity == "light":
        duration = 35
    elif activity == "moderate":
        duration = 30
    else:  # active
        duration = 25

    # Slight tweak by goal: loss can add 5 min; gain (strength) can be longer
    if goal == "loss" and exercise_type == "Cardio":
        duration = min(50, duration + 5)
    if goal == "gain" and exercise_type == "Strength":
        duration = min(50, duration + 10)

    # --- Frequency (days per week) ---
    # Sedentary/light need more; active need less (already train often)
    if activity == "sedentary":
        frequency = 5
    elif activity == "light":
        frequency = 4
    elif activity == "moderate":
        frequency = 4
    else:  # active
        frequency = 3

    # Gain with strength: 4–5 to support growth
    if goal == "gain" and exercise_type == "Strength":
        frequency = 4

    return {
        "exercise_type": exercise_type,
        "exercise_duration": duration,
        "exercise_frequency": frequency,
    }
