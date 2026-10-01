from backend.models.base_model import BaseModel

DETAILS = '''SELECT r.id,r.user_id,r.status_id,r.created_at,r.payment_method,
 u.login,u.fio,e.name,e.date,e.start_time,e.place,s.name AS status,
 v.text AS review_text,v.rating AS review_rating
 FROM request r JOIN user u ON u.id=r.user_id JOIN event e ON e.id=r.event_id
 JOIN status s ON s.id=r.status_id LEFT JOIN review v ON v.request_id=r.id'''


class Request(BaseModel):
    def __init__(self, user_id, event_id, payment_method, db=None):
        super().__init__(db)
        self.user_id, self.event_id, self.payment_method = user_id, event_id, payment_method

    def validate(self):
        if self.payment_method not in ('При очном посещении','СБП'):
            return False, 'Выберите способ оплаты'
        if not self.db.fetch_one('SELECT id FROM event WHERE id=?',(self.event_id,)):
            return False, 'Мероприятие не найдено'
        return True, ''

    def save(self):
        ok, msg = self.validate()
        if not ok:
            return False, msg
        self.id = self.db.execute('INSERT INTO request(user_id,event_id,payment_method) VALUES(?,?,?)',
                                  (self.user_id,self.event_id,self.payment_method))
        return True, self.id

    @staticmethod
    def for_user(db, user_id):
        return db.fetch_all(DETAILS+' WHERE r.user_id=? ORDER BY r.id DESC', (user_id,))

    @staticmethod
    def all(db):
        return db.fetch_all(DETAILS+' ORDER BY r.id DESC')

    @staticmethod
    def update_status(db, request_id, status_id):
        if type(status_id) is not int or status_id not in (1,2,3):
            return False, 'Некорректный статус'
        row = db.fetch_one('SELECT status_id FROM request WHERE id=?',(request_id,))
        if not row:
            return False, 'Заявка не найдена'
        if status_id < row['status_id']:
            return False, 'Нельзя вернуть заявку на предыдущий этап'
        db.execute('UPDATE request SET status_id=? WHERE id=?',(status_id,request_id))
        return True, ''
