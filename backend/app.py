import hmac
import os
import secrets
import time
from datetime import timedelta
from flask import Flask, session, request, g, jsonify, redirect
from backend.database import ROOT
from init_db import initialize, ensure_env


def create_app(config=None):
    ensure_env()
    app=Flask(__name__,template_folder=str(ROOT/'frontend/templates'),static_folder=str(ROOT/'frontend/static'))
    app.config.update(SECRET_KEY=os.environ['FLASK_SECRET_KEY'],SESSION_COOKIE_NAME='conf_session',
                      SESSION_COOKIE_HTTPONLY=True,SESSION_COOKIE_SAMESITE='Lax',
                      SESSION_COOKIE_SECURE=os.environ.get('COOKIE_SECURE')=='1',
                      PERMANENT_SESSION_LIFETIME=timedelta(minutes=30),MAX_CONTENT_LENGTH=16384,
                      DATABASE_PATH=os.environ.get('DATABASE_PATH',str(ROOT/'database/conference.db')))
    if config:
        app.config.update(config)
    app.db=initialize(app.config['DATABASE_PATH'])

    @app.before_request
    def protect():
        g.user=None
        if session.get('user_id'):
            user=app.db.fetch_one('SELECT id,login,role,session_version FROM user WHERE id=?',(session['user_id'],))
            elapsed=time.time()-session.get('last_seen',0)
            if not user or elapsed>1800 or session.get('version') != user['session_version']:
                session.clear()
            else:
                g.user=user
                session['last_seen']=time.time()
        if request.method in ('POST','PUT','DELETE','PATCH'):
            expected=session.get('csrf','')
            supplied=request.headers.get('X-CSRF-Token','')
            if not expected or not hmac.compare_digest(expected,supplied):
                return jsonify(success=False,message='Обновите страницу: неверный CSRF-токен'),400

    def csrf_token():
        if 'csrf' not in session:
            session['csrf']=secrets.token_urlsafe(32)
        return session['csrf']
    app.jinja_env.globals['csrf_token']=csrf_token

    @app.after_request
    def headers(response):
        response.headers['X-Content-Type-Options']='nosniff'
        response.headers['X-Frame-Options']='DENY'
        response.headers['Referrer-Policy']='same-origin'
        response.headers['Content-Security-Policy']="default-src 'self'; script-src 'self'; style-src 'self'; frame-ancestors 'none'; form-action 'self'; base-uri 'self'"
        response.headers['Cache-Control']='no-store'
        return response

    from backend.routes.auth_routes import auth_bp
    from backend.routes.request_routes import request_bp
    from backend.routes.admin_routes import admin_bp
    app.register_blueprint(auth_bp,url_prefix='/api/auth')
    app.register_blueprint(request_bp)
    app.register_blueprint(admin_bp)

    @app.get('/')
    def index():
        return redirect('/admin' if g.user and g.user['role']=='admin' else '/dashboard' if g.user else '/api/auth/login')

    return app


if __name__=='__main__':
    create_app().run(host='127.0.0.1',port=int(os.environ.get('PORT','5000')),debug=False)
