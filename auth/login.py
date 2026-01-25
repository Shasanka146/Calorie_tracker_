"""
User login logic.
"""
from werkzeug.security import check_password_hash
from database.db_helper import get_user_by_username


def authenticate_user(username, password):
    """
    Authenticate a user.
    Returns (success: bool, message: str, user: dict or None)
    """
    if not username or not username.strip():
        return False, "Username is required.", None
    
    if not password:
        return False, "Password is required.", None
    
    username = username.strip().lower()
    
    # Get user from database
    user = get_user_by_username(username)
    
    if not user:
        return False, "Invalid username or password.", None
    
    # Check password
    if check_password_hash(user["password_hash"], password):
        return True, "Login successful!", dict(user)
    else:
        return False, "Invalid username or password.", None
