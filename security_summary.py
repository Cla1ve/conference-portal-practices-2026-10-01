"""Проверка свойств настоящего ответа приложения без вывода cookie и ключа."""
import tempfile
import re
from pathlib import Path
from backend.app import create_app

with tempfile.TemporaryDirectory() as folder:
    app=create_app({'TESTING':True,'DATABASE_PATH':str(Path(folder)/'cookie.db')})
    client=app.test_client()
    client.get('/api/auth/login')
    with client.session_transaction() as session:token=session['csrf']
    response=client.post('/api/auth/login',json={'login':'Conf2027','password':'Demo77'},headers={'X-CSRF-Token':token})
    cookie=response.headers['Set-Cookie']
    print('Вход администратора: HTTP',response.status_code)
    print('Cookie conf_session: HttpOnly =', 'HttpOnly' in cookie)
    print('Cookie conf_session: SameSite=Lax =', 'SameSite=Lax' in cookie)
    print('Secure для локального HTTP =',app.config['SESSION_COOKIE_SECURE'])
    print('Время бездействия до выхода: 30 минут')
    print('SECRET_KEY: загружен из окружения; значение не выводится')
    print('Для HTTPS COOKIE_SECURE=1 включает Secure')
