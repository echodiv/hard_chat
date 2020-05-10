CREATE TABLE IF NOT EXISTS users
    (uid             INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
     reg_time        DATETIME NOT NULL, --YYYY-MM-DD HH:MM:SS.SSS
     last_visit_time DATETIME,
     name            TEXT,
     sename          TEXT,
     email           TEXT,
     password        TEXT,
     salt            TEXT,
     phone           TEXT,
     status          SMALLINT);

CREATE UNIQUE INDEX user_id ON users(uid);

CREATE TABLE IF NOT EXISTS chats
    (chat_id     INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
     create_time DATETIME NOT NULL,
     name        TEXT,
     status      SMALLINT,
     description TEXT);

CREATE TABLE IF NOT EXISTS messages
    (message_id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
     timestamp  DATETIME NOT NULL,
     message    TEXT,
     type       SMALLINT,
     status     SMALLINT,
     FOREIGN KEY(uid)     REFERENCES users(uid),
     FOREIGN KEY(chat_id) REFERENCES chats(chat_id));

CREATE TABLE IF NOT EXISTS talkers
    (user_role SMALLINT,
     satus     SMALLINT,
     FOREIGN KEY(chat_id) REFERENCES chats(chat_id),
     FOREIGN KEY(uid)     REFERENCES users(uid));

