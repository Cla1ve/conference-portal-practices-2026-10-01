"""Отдельная учебная БД практической 2. Рабочую БД сайта не изменяет."""
from init_db import initialize
from backend.database import ROOT
from backend.models.user import User
from backend.models.event import Event
from backend.models.request import Request

db=initialize(ROOT/'database/sample.db')
user=db.fetch_one('SELECT id FROM user WHERE login=?',('student2027',))
if not user:
    ok,uid=User('student2027','Student2027','Иванов Иван Иванович','student@example.ru','8(999)123-45-67',db).save()
else:uid=user['id']
ok,eid=Event('Аудитория №101','2027-06-15','10:00','Аудитория',db).save()
if not db.fetch_one('SELECT id FROM request WHERE user_id=?',(uid,)):
    Request(uid,eid,'СБП',db).save()
print('Учебная база sample.db создана. Таблицы: event request review status user')
for row in db.fetch_all('SELECT r.id,u.login,e.name,e.date,e.start_time,r.payment_method,s.name AS status FROM request r JOIN user u ON u.id=r.user_id JOIN event e ON e.id=r.event_id JOIN status s ON s.id=r.status_id'):
    print(row)
print('Проверка целостности:',db.fetch_one('PRAGMA integrity_check'))
print('Ошибки внешних ключей:',db.fetch_all('PRAGMA foreign_key_check'))
