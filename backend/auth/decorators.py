from functools import wraps
from flask import g, jsonify, redirect, request


def login_required(func):
    @wraps(func)
    def wrapper(*args,**kwargs):
        if g.user is None:
            if request.path.startswith('/api/'):
                return jsonify(success=False,message='Требуется вход'),401
            return redirect('/api/auth/login')
        return func(*args,**kwargs)
    return wrapper


def admin_required(func):
    @wraps(func)
    @login_required
    def wrapper(*args,**kwargs):
        if g.user['role'] != 'admin':
            return jsonify(success=False,message='Доступ запрещён'),403
        return func(*args,**kwargs)
    return wrapper


def participant_required(func):
    @wraps(func)
    @login_required
    def wrapper(*args,**kwargs):
        if g.user['role'] != 'user':
            return jsonify(success=False,message='Раздел доступен участнику'),403
        return func(*args,**kwargs)
    return wrapper
