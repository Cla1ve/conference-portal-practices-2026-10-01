from backend.models.base_model import BaseModel


class Status(BaseModel):
    def __init__(self, name, db=None):
        super().__init__(db)
        self.name = name

    def validate(self):
        return (self.name in ('Новая','Мероприятие назначено','Завершено'), 'Некорректный статус')

    def save(self):
        ok, msg = self.validate()
        if not ok:
            return False, msg
        self.id = self.db.fetch_one('SELECT id FROM status WHERE name=?', (self.name,))['id']
        return True, self.id
