# Таблицы базы Конференции РФ

Пять сущностей из практической дополнены полями из ТЗ на страницах 29–31.
Мероприятие хранит выбранное помещение, дату и время начала. Заявка хранит способ оплаты.
SQLite хранит DATE и DATETIME в текстовом формате ISO. VARCHAR имеет текстовую
аффинность; длину и формат проверяет сервер, для логина также задан CHECK.

| Таблица | Поля и ограничения |
|---|---|
| user | id INTEGER PK; login VARCHAR(50) UNIQUE NOT NULL; password_hash VARCHAR(255) NOT NULL; fio VARCHAR(150) NOT NULL; email VARCHAR(100) UNIQUE NOT NULL; phone VARCHAR(18) NOT NULL; role VARCHAR(20) NOT NULL DEFAULT user CHECK user/admin; session_version INTEGER NOT NULL DEFAULT 0 |
| event | id INTEGER PK; name VARCHAR(200) NOT NULL; date DATE NOT NULL; start_time VARCHAR(5) NOT NULL; place VARCHAR(200) NOT NULL CHECK Аудитория/Коворкинг/Кинозал; description TEXT NOT NULL DEFAULT пустая строка; UNIQUE(name,date,start_time,place) |
| status | id INTEGER PK; name VARCHAR(50) UNIQUE NOT NULL; фиксированные значения 1 Новая, 2 Мероприятие назначено, 3 Завершено |
| request | id INTEGER PK; user_id INTEGER FK user.id NOT NULL; event_id INTEGER FK event.id NOT NULL; status_id INTEGER FK status.id NOT NULL DEFAULT 1; payment_method VARCHAR(30) NOT NULL CHECK При очном посещении/СБП; created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP |
| review | id INTEGER PK; request_id INTEGER FK request.id UNIQUE NOT NULL; text TEXT NOT NULL CHECK 1–2000 символов; rating INTEGER NOT NULL CHECK 1–5; created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP |

PK всех таблиц: id. Для user, event, request, review включён AUTOINCREMENT.
Связи: user 1:M request, event 1:M request, status 1:M request.
request 1:0..1 review: отзыв необязателен и может быть только один.
user M:N event реализуется через request.
Все поля атомарны. Неключевые поля зависят от своего id, названия статусов
не повторяются в заявках. Схема соответствует 1НФ, 2НФ и 3НФ.
