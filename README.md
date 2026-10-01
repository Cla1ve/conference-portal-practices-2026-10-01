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

## Отчёты и результаты

`reports/` содержит четыре отчёта Word и PDF по шаблону колледжа.
`screenshots/` содержит реальные снимки сайта и окон терминала SQLite и Python.
`browser-results.json` содержит результат проверки полного сценария в браузере
и фактические признаки session cookie, без её значения.
Все 22 автоматические проверки выполнены успешно.

Источники задания: [ТЗ, страницы 29–31](https://github.com/softboxdev/web_development_course/blob/main/%D0%9A%D0%98%D0%9C%2009.02.07-3-2027%20%D0%A2%D0%BE%D0%BC%201.pdf),
[ER](https://github.com/softboxdev/web_development_course/blob/main/practice_er_datagrams.md),
[SQLite](https://github.com/softboxdev/web_development_course/blob/main/practice_sql_database_preparation.md),
[модули](https://github.com/softboxdev/web_development_course/blob/main/information_system_modules.md),
[безопасность](https://github.com/softboxdev/web_development_course/blob/main/practice_security_sessions.md).
