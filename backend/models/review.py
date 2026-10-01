import sqlite3
from backend.models.base_model import BaseModel


class Review(BaseModel):
    def __init__(self, request_id, user_id, text, rating, db=None):
        super().__init__(db)
        self.request_id,self.user_id,self.text,self.rating = request_id,user_id,text,rating

    def validate(self):
        row = self.db.fetch_one('SELECT * FROM request WHERE id=?',(self.request_id,))
        if not row or row['user_id'] != self.user_id:
            return False, 'Заявка не найдена'
        if row['status_id'] != 3:
            return False, 'Отзыв доступен после завершения мероприятия'
        if not isinstance(self.text,str) or not 1 <= len(self.text.strip()) <= 2000:
            return False, 'Текст отзыва должен содержать от 1 до 2000 символов'
        if type(self.rating) is not int or not 1 <= self.rating <= 5:
            return False, 'Оценка должна быть целым числом от 1 до 5'
        if self.db.fetch_one('SELECT id FROM review WHERE request_id=?',(self.request_id,)):
            return False, 'Отзыв уже добавлен'
        return True, ''

    def save(self):
        ok,msg = self.validate()
        if not ok:
            return False,msg
        try:
            self.id=self.db.execute('INSERT INTO review(request_id,text,rating) VALUES(?,?,?)',
                                    (self.request_id,self.text.strip(),self.rating))
        except sqlite3.IntegrityError:
            return False,'Отзыв уже добавлен'
        return True,self.id
