import re
import tempfile
import time
import unittest
from pathlib import Path
from backend.app import create_app
from backend.database import Database
from backend.models.user import User
from backend.models.base_model import BaseModel
from werkzeug.security import check_password_hash


class PortalTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.tmp=tempfile.TemporaryDirectory()
        cls.app=create_app({'TESTING':True,'SECRET_KEY':'test-only-key','DATABASE_PATH':str(Path(cls.tmp.name)/'test.db')})
        cls.db=cls.app.db
        cls.payload={'login':'student2027','password':'Student2027','fio':'Иванов Иван Иванович','email':'student@example.ru','phone':'8(999)123-45-67'}
        User(**cls.payload,db=cls.db).save()

    @classmethod
    def tearDownClass(cls):
        cls.tmp.cleanup()

    def setUp(self):
        self.client=self.app.test_client()
        self.client.get('/api/auth/login')

    def token(self,client=None):
        with (client or self.client).session_transaction() as s:
            return s['csrf']

    def send(self,url,data,method='POST',client=None):
        c=client or self.client
        return c.open(url,method=method,json=data,headers={'X-CSRF-Token':self.token(c)})

    def login(self,login='student2027',password='Student2027'):
        return self.send('/api/auth/login',{'login':login,'password':password})

    def booking(self):
        return self.send('/api/requests',{'name':'Аудитория №101','date':'2027-06-15','start_time':'10:00','place':'Аудитория','payment_method':'СБП'})

    def test_01_schema(self):
        tables=self.db.fetch_all("SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%'")
        self.assertEqual({x['name'] for x in tables},{'user','event','status','request','review'})
        self.assertEqual(self.db.fetch_one('PRAGMA foreign_keys')['foreign_keys'],1)
        self.assertEqual(self.db.fetch_all('PRAGMA foreign_key_check'),[])

    def test_02_hash(self):
        u=self.db.fetch_one('SELECT password_hash FROM user WHERE login=?',('student2027',))
        self.assertTrue(u['password_hash'].startswith('pbkdf2:sha256:600000$'))
        self.assertNotEqual(u['password_hash'],'Student2027')
        self.assertTrue(check_password_hash(u['password_hash'],'Student2027'))
        self.assertFalse(check_password_hash(u['password_hash'],'wrong'))

    def test_03_sql_injection(self):
        self.assertEqual(self.db.fetch_all('SELECT id FROM user WHERE login=?',("' OR '1'='1",)),[])
        self.assertEqual(self.login("' OR '1'='1",'anything').status_code,401)

    def test_04_guest(self):
        self.assertEqual(self.client.get('/dashboard').status_code,302)
        self.assertEqual(self.client.get('/api/requests').status_code,401)

    def test_05_registration_validation(self):
        for field,value in [('login','abc'),('password','123'),('fio','John Doe'),('phone','+79991234567'),('email','invalid')]:
            with self.subTest(field=field):
                d={**self.payload,field:value}
                self.assertEqual(self.send('/api/auth/register',d).status_code,400)

    def test_06_duplicate(self):
        self.assertEqual(self.send('/api/auth/register',self.payload).status_code,400)

    def test_07_login_error(self):
        self.assertEqual(self.login(password='wrong').status_code,401)

    def test_08_admin_login(self):
        r=self.login('Conf2027','Demo77')
        self.assertEqual(r.json['redirect'],'/admin')
        self.assertEqual(self.client.get('/admin').status_code,200)

    def test_09_participant_cannot_admin(self):
        self.login()
        self.assertEqual(self.client.get('/admin').status_code,403)
        self.assertEqual(self.send('/api/admin/requests/1',{'status_id':3},'PUT').status_code,403)

    def test_10_booking_and_review(self):
        self.login()
        r=self.booking();self.assertEqual(r.status_code,201);rid=r.json['request_id']
        self.assertEqual(self.db.fetch_one('SELECT status_id,payment_method FROM request WHERE id=?',(rid,)),{'status_id':1,'payment_method':'СБП'})
        self.assertEqual(self.send(f'/api/requests/{rid}/review',{'text':'Спасибо','rating':5}).status_code,400)
        self.login('Conf2027','Demo77')
        self.assertEqual(self.send(f'/api/admin/requests/{rid}',{'status_id':2},'PUT').status_code,200)
        self.assertEqual(self.send(f'/api/admin/requests/{rid}',{'status_id':3},'PUT').status_code,200)
        self.login()
        self.assertEqual(self.send(f'/api/requests/{rid}/review',{'text':'Спасибо','rating':5}).status_code,201)
        self.assertEqual(self.send(f'/api/requests/{rid}/review',{'text':'Повтор','rating':5}).status_code,400)

    def test_11_other_user_isolation(self):
        self.login();rid=self.booking().json['request_id']
        self.send('/api/auth/register',{**self.payload,'login':'another2027','email':'other@example.ru'})
        self.login('another2027','Student2027')
        self.assertNotIn(rid,[r['id'] for r in self.client.get('/api/requests').json['requests']])
        self.assertEqual(self.send(f'/api/requests/{rid}/review',{'text':'Чужая','rating':5}).status_code,400)

    def test_12_invalid_booking(self):
        self.login()
        for data in [{},{'name':'X','date':'bad','place':'Другое'},{'name':'Комната','date':'2020-01-01','start_time':'10:00','place':'Аудитория','payment_method':'СБП'}]:
            self.assertEqual(self.send('/api/requests',data).status_code,400)

    def test_13_csrf(self):
        self.assertEqual(self.client.post('/api/auth/login',json={'login':'Conf2027','password':'Demo77'}).status_code,400)

    def test_14_cookie_flags(self):
        r=self.login()
        cookie=r.headers['Set-Cookie']
        self.assertIn('HttpOnly',cookie);self.assertIn('SameSite=Lax',cookie)
        self.assertEqual(self.app.config['PERMANENT_SESSION_LIFETIME'].total_seconds(),1800)
        self.assertFalse(self.app.config['SESSION_COOKIE_SECURE'])

    def test_15_cookie_tampering(self):
        self.login()
        self.client.set_cookie('conf_session','tampered.value.signature')
        self.assertEqual(self.client.get('/api/requests').status_code,401)

    def test_16_idle_timeout(self):
        self.login()
        with self.client.session_transaction() as s:s['last_seen']=time.time()-1801
        self.assertEqual(self.client.get('/api/requests').status_code,401)

    def test_17_logout_replay(self):
        self.login();old=self.client.get_cookie('conf_session').value
        self.assertEqual(self.send('/api/auth/logout',{}).status_code,200)
        self.client.set_cookie('conf_session',old)
        self.assertEqual(self.client.get('/api/requests').status_code,401)

    def test_18_role_not_from_input(self):
        r=self.send('/api/auth/register',{**self.payload,'login':'safeuser2027','email':'safe@example.ru','role':'admin'})
        self.assertEqual(r.status_code,201)
        self.assertEqual(self.db.fetch_one('SELECT role FROM user WHERE id=?',(r.json['user_id'],))['role'],'user')

    def test_19_missing_status(self):
        self.login('Conf2027','Demo77')
        for status in [None,'3',True,4]:
            self.assertEqual(self.send('/api/admin/requests/99999',{'status_id':status},'PUT').status_code,400)
        self.assertEqual(self.send('/api/admin/requests/99999',{'status_id':3},'PUT').status_code,400)

    def test_20_foreign_key(self):
        import sqlite3
        with self.assertRaises(sqlite3.IntegrityError):
            self.db.execute('INSERT INTO request(user_id,event_id,payment_method) VALUES(?,?,?)',(999999,999999,'СБП'))

    def test_21_oop_and_singleton(self):
        self.assertTrue(issubclass(User,BaseModel))
        self.assertIs(Database(self.db.db_path),self.db)

    def test_22_xss_escape(self):
        self.login();rid=self.booking().json['request_id']
        self.login('Conf2027','Demo77');self.send(f'/api/admin/requests/{rid}',{'status_id':3},'PUT')
        self.login();self.send(f'/api/requests/{rid}/review',{'text':'<script>alert(1)</script>','rating':5})
        text=self.client.get('/dashboard').text
        self.assertIn('&lt;script&gt;alert(1)&lt;/script&gt;',text)
        self.assertNotIn('<script>alert(1)</script>',text)


if __name__=='__main__':unittest.main(verbosity=2)
