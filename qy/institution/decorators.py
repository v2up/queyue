from functools import wraps

from itsdangerous import URLSafeSerializer
from flask import abort, request, current_app
from ..models import Institution

def insti_required(f):
    def decorator(f):
        @wraps(f)
        def decorated_func(*args, **kwargs):
            if current_insti() is None:
                abort(403)
            return f(*args, **kwargs)
        return decorated_func
    return decorator

def current_insti():
    insti_uurl = request.cookies.get('insti-uurl')
    if insti_uurl:
        s = URLSafeSerializer(current_app.config['SECRET_KEY'])
        uurl = s.loads(insti_uurl)
        return Institution.query.filter_by(uurl=uurl).first()
    return None