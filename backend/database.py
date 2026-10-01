import os
import sqlite3
from contextlib import contextmanager
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class Database:
    """Один объект доступа к БД; отдельное соединение для каждого запроса."""
    _instances = {}

    def __new__(cls, db_path=None):
        path = str(Path(db_path or os.environ.get('DATABASE_PATH', ROOT / 'database/conference.db')).resolve())
        if path not in cls._instances:
            instance = super().__new__(cls)
            instance.db_path = path
            cls._instances[path] = instance
        return cls._instances[path]

    @contextmanager
    def get_connection(self):
        conn = sqlite3.connect(self.db_path, timeout=10)
        conn.row_factory = sqlite3.Row
        conn.execute('PRAGMA foreign_keys = ON')
        try:
            with conn:
                yield conn
        finally:
            conn.close()

    def execute(self, query, params=()):
        with self.get_connection() as conn:
            return conn.execute(query, params).lastrowid

    def fetch_one(self, query, params=()):
        with self.get_connection() as conn:
            row = conn.execute(query, params).fetchone()
            return dict(row) if row else None

    def fetch_all(self, query, params=()):
        with self.get_connection() as conn:
            return [dict(row) for row in conn.execute(query, params).fetchall()]
