import logging

from db.database import Database


class db_user_functions(Database):
    def __init__(self):
        super().__init__()

    def check_users(self, chat_id):
        try:
            self.cursor.execute("SELECT * FROM users WHERE chat_id = ?", (chat_id,))
            user = self.cursor.fetchone()
            return user is not None
        except Exception as e:
            logging.error(f"Ошибка при проверке наличия пользователя: {e}")
            raise Exception(f"Произошла ошибка при проверке наличия пользователя: {e}")

    def add_user(self, chat_id, username):
        try:
            self.cursor.execute("INSERT INTO users (chat_id, username) VALUES (?, ?)", (chat_id, username))
            self.conn.commit()
        except Exception as e:
            logging.error(f"Ошибка при добавлении пользователя: {e}")
            raise Exception(f"Произошла ошибка при добавлении пользователя: {e}")
