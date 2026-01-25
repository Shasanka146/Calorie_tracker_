"""
User registration logic.
"""
from werkzeug.security import generate_password_hash
from database.db_helper import create_user, get_user_by_username, get_user_by_email
import re


def validate_email(email):
    """Basic email validation."""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None


def validate_password(password):
    """Validate password strength."""
    if len(password) < 6:
        return False, "Password must be at least 6 characters long."
    return True, ""


def register_user(username, email, password):
    """
    Register a new user.
    Returns (success: bool, message: str, user_id: int or None)
    """
    # Validate inputs
    if not username or not username.strip():
        return False, "Username is required.", None
    
    if not email or not email.strip():
        return False, "Email is required.", None
    
    if not password:
        return False, "Password is required.", None
    
    username = username.strip().lower()
    email = email.strip().lower()
    
    # Validate email format
    if not validate_email(email):
        return False, "Invalid email format.", None
    
    # Validate password
    is_valid, error_msg = validate_password(password)
    if not is_valid:
        return False, error_msg, None
    
    # Check if username already exists
    if get_user_by_username(username):
        return False, "Username already exists. Please choose another.", None
    
    # Check if email already exists
    if get_user_by_email(email):
        return False, "Email already registered. Please use another email.", None
    
    # Hash password
    password_hash = generate_password_hash(password)
    
    # Create user
    user_id = create_user(username, email, password_hash)
    
    if user_id:
        return True, "Registration successful! Please login.", user_id
    else:
        return False, "Registration failed. Please try again.", None
