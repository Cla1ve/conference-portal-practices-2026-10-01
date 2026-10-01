import os
import secrets
from pathlib import Path
from dotenv import load_dotenv
from werkzeug.security import generate_password_hash
from backend.database import Database, ROOT


def initialize(path=None):
    db = Database(path)
    Path(db.db_path).parent.mkdir(parents=True,exist_ok=True)
    with db.get_connection() as conn:
        conn.executescript((ROOT/'schema.sql').read_text(encoding='utf-8'))
        if not conn.execute('SELECT id FROM user WHERE login=?',('Conf2027',)).fetchone():
            conn.execute('INSERT INTO user(login,password_hash,fio,email,phone,role) VALUES(?,?,?,?,?,?)',
                ('Conf2027',generate_password_hash('Demo77',method='pbkdf2:sha256:600000'),
                 'Администратор портала','admin@example.ru','8(999)000-00-00','admin'))
    return db


def ensure_env():
    env_path=ROOT/'.env'
    if not env_path.exists():
        env_path.write_text('FLASK_SECRET_KEY='+secrets.token_hex(32)+'\nCOOKIE_SECURE=0\n',encoding='utf-8')
    load_dotenv(env_path)


if __name__=='__main__':
    ensure_env()
    db=initialize()
    print('SQLite база:',db.db_path)
    print('Таблицы:',', '.join(x['name'] for x in db.fetch_all("SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%' ORDER BY name")))
    print('PRAGMA foreign_keys: 1; администратор Conf2027 создан или уже существует')
