import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash
from backend.models.base_model import BaseModel
from backend.database import Database
from backend.validators.validators import Validator


class User(BaseModel):
    def __init__(self, login, password, fio, email, phone, db=None):
        super().__init__(db)
        self.login = login.strip() if isinstance(login, str) else login
        self.password = password
        self.fio = fio.strip() if isinstance(fio, str) else fio
        self.email = email.strip().lower() if isinstance(email, str) else email
        self.phone = phone.strip() if isinstance(phone, str) else phone

    def validate(self):
        return Validator.registration(self)

    def save(self):
        ok, message = self.validate()
        if not ok:
            return False, message
        if self.db.fetch_one('SELECT id FROM user WHERE login=?', (self.login,)):
            return False, 'Пользователь с таким логином уже существует'
        if self.db.fetch_one('SELECT id FROM user WHERE email=?', (self.email,)):
            return False, 'Пользователь с таким email уже существует'
        hashed = generate_password_hash(self.password, method='pbkdf2:sha256:600000', salt_length=16)
        try:
            self.id = self.db.execute(
                'INSERT INTO user(login,password_hash,fio,email,phone,role) VALUES(?,?,?,?,?,?)',
                (self.login, hashed, self.fio, self.email, self.phone, 'user'))
        except sqlite3.IntegrityError:
            return False, 'Логин или email уже занят'
        return True, self.id

    @staticmethod
    def authenticate(login, password, db=None):
        if not isinstance(login, str) or not isinstance(password, str) or len(password) > 128:
            return None
        db = db or Database()
        user = db.fetch_one('SELECT * FROM user WHERE login=?', (login.strip(),))
        return user if user and check_password_hash(user['password_hash'], password) else None
