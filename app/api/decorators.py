from functools import wraps
from flask import g
from .errors import forbidden


def permission_required(permission):
    def decorater(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not g.current_user.can(permission):
                return forbidden('Insufficient permission')
            return f(*args, **kwargs)
        return decorated_function
    return decorater