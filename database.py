import sqlite3
import pandas as pd
import openpyxl


class Database:
    def __init__(self):
        # Подключение к базе данных
        self.conn = sqlite3.connect('users.db', check_same_thread=False)
        # Курсор взаимодействия с БД
        self.cursor = self.conn.cursor()
        self.create_users_table()

    def create_users_table(self):
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            chat_id INTEGER NOT NULL,
            username TEXT NOT NULL,
        )''')
        self.conn.commit()


    # Метод для закрытия соединения
    def close_connection(self):
        self.conn.close()

