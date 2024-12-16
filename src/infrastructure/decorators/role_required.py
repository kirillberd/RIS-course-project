from functools import wraps
from flask import session, abort

#TODO переделать декоратор
def role_required(role):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            user_role = session["role"]
            if user_role != role:
                abort(403)
            return func(*args, **kwargs)
        return wrapper
    return decorator