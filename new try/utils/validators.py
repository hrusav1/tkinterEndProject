#/utils/validators.py
import re

def validate_email(email):
    pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    return re.match(pattern, email) is not None

def validate_password(password):
    return len(password) >= 8

def validate_apiary_name(name):
    return len(name) > 0 and len(name) <= 100

def validate_number_of_hives(num_hives):
    try:
        num = int(num_hives)
        return num > 0
    except ValueError:
        return False

# Add more validation functions as needed