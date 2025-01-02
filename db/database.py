import sqlite3


class Database:
    def __init__(self):
        # Подключение к базе данных
        self.conn = sqlite3.connect('users.db', check_same_thread=False)
        # Курсор взаимодействия с БД
        self.cursor = self.conn.cursor()
        self.cursor.execute('PRAGMA foreign_keys = ON;')
        self.create_users_table()
        self.create_channels_table()

    def create_users_table(self):
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            chat_id INTEGER NOT NULL UNIQUE,
            username TEXT NOT NULL UNIQUE
        )''')
        self.conn.commit()

    def create_channels_table(self):
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS channels (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            chat_id INTEGER,
            channel_name TEXT NOT NULL,
            FOREIGN KEY (chat_id) REFERENCES users (chat_id)
        )''')
        self.conn.commit()

    # Метод для закрытия соединения
    def close_connection(self):
        self.conn.close()


class DatabaseExeption(Exception):
    pass
