from backend.models.base_model import BaseModel
from backend.validators.validators import Validator


class Event(BaseModel):
    def __init__(self, name, date, start_time, place, db=None):
        super().__init__(db)
        self.name, self.date, self.start_time, self.place = name, date, start_time, place

    def validate(self):
        return Validator.event(self)

    def save(self):
        ok, msg = self.validate()
        if not ok:
            return False, msg
        self.db.execute('INSERT OR IGNORE INTO event(name,date,start_time,place) VALUES(?,?,?,?)',
                        (self.name.strip(), self.date, self.start_time, self.place))
        self.id = self.db.fetch_one('SELECT id FROM event WHERE name=? AND date=? AND start_time=? AND place=?',
                                    (self.name.strip(), self.date, self.start_time, self.place))['id']
        return True, self.id
