PRAGMA foreign_keys = ON;
CREATE TABLE IF NOT EXISTS user (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    login VARCHAR(50) UNIQUE NOT NULL CHECK(length(login) BETWEEN 6 AND 50),
    password_hash VARCHAR(255) NOT NULL,
    fio VARCHAR(150) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    phone VARCHAR(18) NOT NULL,
    role VARCHAR(20) NOT NULL DEFAULT 'user' CHECK(role IN ('user','admin')),
    session_version INTEGER NOT NULL DEFAULT 0
);
CREATE TABLE IF NOT EXISTS event (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(200) NOT NULL,
    date DATE NOT NULL,
    start_time VARCHAR(5) NOT NULL,
    place VARCHAR(200) NOT NULL CHECK(place IN ('Аудитория','Коворкинг','Кинозал')),
    description TEXT NOT NULL DEFAULT '',
    UNIQUE(name,date,start_time,place)
);
CREATE TABLE IF NOT EXISTS status (
    id INTEGER PRIMARY KEY,
    name VARCHAR(50) UNIQUE NOT NULL
);
INSERT OR IGNORE INTO status(id,name) VALUES
    (1,'Новая'),(2,'Мероприятие назначено'),(3,'Завершено');
CREATE TABLE IF NOT EXISTS request (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL REFERENCES user(id),
    event_id INTEGER NOT NULL REFERENCES event(id),
    status_id INTEGER NOT NULL DEFAULT 1 REFERENCES status(id),
    payment_method VARCHAR(30) NOT NULL CHECK(payment_method IN ('При очном посещении','СБП')),
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP
);
CREATE INDEX IF NOT EXISTS request_user_idx ON request(user_id);
CREATE INDEX IF NOT EXISTS request_event_idx ON request(event_id);
CREATE INDEX IF NOT EXISTS request_status_idx ON request(status_id);
CREATE TABLE IF NOT EXISTS review (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    request_id INTEGER UNIQUE NOT NULL REFERENCES request(id),
    text TEXT NOT NULL CHECK(length(text) BETWEEN 1 AND 2000),
    rating INTEGER NOT NULL CHECK(rating BETWEEN 1 AND 5),
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP
);
