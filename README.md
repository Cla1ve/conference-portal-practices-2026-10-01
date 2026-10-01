# Конференции РФ

Практические работы 1–4. Маматисаков Элмурат Сапарбекович, 4ИСП9-45.

Портал позволяет зарегистрироваться, войти, отправить заявку на помещение,
просмотреть свои заявки и оставить отзыв после завершения мероприятия.
Администратор видит все заявки и меняет статус.

## Запуск Windows

```powershell
python -m venv .venv
.venv\Scripts\python -m pip install -r requirements.txt
.venv\Scripts\python init_db.py
.venv\Scripts\python -m backend.app
```

Открыть http://127.0.0.1:5000. Администратор: Conf2027 / Demo77 (из учебного ТЗ).
Для участника создайте учётную запись в форме регистрации.
Пароль участника не короче 8 символов; исключение Demo77 касается только
заранее заданного в ТЗ администратора.

## Запуск РОСА Линукс

```bash
sudo dnf install python3 python3-pip sqlite3 git
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python init_db.py
python -m backend.app
```

Проверено на Windows, Python 3.12. Проект использует переносимые Python и SQLite.
init_db.py создаёт пять таблиц и администратора, существующие данные сохраняет.
Секретный ключ случайно создаётся в локальном .env при первом запуске.
.env и рабочая БД не отправляются в Git. Для HTTPS задайте COOKIE_SECURE=1.

## Файлы и проверки

frontend — HTML/CSS/JS; backend — Flask, модели с BaseModel и валидаторы;
database — SQLite. Database использует Singleton и включает FK при подключении.
schema.sql — схема; tables.md — поля и связи; er_diagram.drawio — редактируемая схема.
database/sample.db — отдельная база с учебными данными для практической 2.
```bash
python -m unittest discover -s tests -v
python test_hash.py
python test_sql_injection.py
```

Для повторного опыта с пустой базой используйте копию проекта без conference.db.
Все пользовательские значения SQL передаются параметрами ?. CSRF-токен проверяется
на изменяющих запросах. Отзывы и списки выводятся с HTML-экранированием.
Сессия действует 30 минут бездействия; при входе и выходе меняется версия
сессии пользователя, поэтому предыдущая cookie теряет доступ.
