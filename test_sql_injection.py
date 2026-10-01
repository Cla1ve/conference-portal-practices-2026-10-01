from backend.database import Database
db=Database()
result=db.fetch_all('SELECT id FROM user WHERE login=?',("' OR '1'='1",))
print('Подготовленный запрос с параметром ?')
print('Результат инъекции:',len(result),'записей')
