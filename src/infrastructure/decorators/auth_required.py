from flask import session, redirect
from functools import wraps
def auth_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        print(session)
        if session.get("username"):
            return func(*args, **kwargs)
        
        return redirect("/auth")
    return wrapper


