from werkzeug.security import generate_password_hash,check_password_hash
hashed=generate_password_hash('Demo77',method='pbkdf2:sha256:600000',salt_length=16)
print('Алгоритм:',hashed.split('$')[0])
print('Хеш:',hashed)
print('Верный пароль:',check_password_hash(hashed,'Demo77'))
print('Неверный пароль:',check_password_hash(hashed,'wrong'))
