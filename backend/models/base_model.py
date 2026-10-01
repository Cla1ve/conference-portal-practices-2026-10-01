from abc import ABC, abstractmethod
from backend.database import Database


class BaseModel(ABC):
    def __init__(self, db=None):
        self.db = db or Database()
        self.id = None

    @abstractmethod
    def validate(self):
        pass

    @abstractmethod
    def save(self):
        pass
