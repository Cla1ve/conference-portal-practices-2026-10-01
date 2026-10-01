import secrets
import time
from flask import Blueprint, current_app, jsonify, render_template, request, session, g
from backend.models.user import User
from backend.auth.decorators import login_required

auth_bp=Blueprint('auth',__name__)


@auth_bp.route('/register',methods=['GET','POST'])
def register():
    if request.method=='GET':
        return render_template('register.html')
    data=request.get_json(silent=True)
    if not isinstance(data,dict):
        return jsonify(success=False,message='Ожидается объект JSON'),400
    user=User(data.get('login'),data.get('password'),data.get('fio'),data.get('email'),data.get('phone'),current_app.db)
    ok,result=user.save()
    return jsonify(success=ok,**({'user_id':result,'message':'Пользователь успешно создан'} if ok else {'message':result})),201 if ok else 400


@auth_bp.route('/login',methods=['GET','POST'])
def login():
    if request.method=='GET':
        return render_template('login.html')
    data=request.get_json(silent=True)
    if not isinstance(data,dict):
        return jsonify(success=False,message='Ожидается объект JSON'),400
    user=User.authenticate(data.get('login'),data.get('password'),current_app.db)
    if not user:
        return jsonify(success=False,message='Неверный логин или пароль'),401
    current_app.db.execute('UPDATE user SET session_version=session_version+1 WHERE id=?',(user['id'],))
    version=current_app.db.fetch_one('SELECT session_version FROM user WHERE id=?',(user['id'],))['session_version']
    session.clear()
    session.update(user_id=user['id'],role=user['role'],login=user['login'],version=version,
                   last_seen=time.time(),csrf=secrets.token_urlsafe(32))
    session.permanent=True
    return jsonify(success=True,role=user['role'],redirect='/admin' if user['role']=='admin' else '/dashboard')


@auth_bp.post('/logout')
@login_required
def logout():
    current_app.db.execute('UPDATE user SET session_version=session_version+1 WHERE id=?',(g.user['id'],))
    session.clear()
    return jsonify(success=True,redirect='/api/auth/login')
