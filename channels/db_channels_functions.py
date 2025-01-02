import logging

from db.database import Database, DatabaseExeption


class db_channels_functions(Database):
    def __init__(self):
        super().__init__()

    def check_channels(self, chat_id):
        try:
            self.cursor.execute("SELECT channel_name FROM channels WHERE chat_id = ?", (chat_id,))
            return self.cursor.fetchall()
        except Exception as e:
            logging.error(f"Ошибка при проверке наличия канала: {e}")
            raise DatabaseExeption(f"Произошла ошибка при проверке наличия канала: {e}")

    def add_channel(self, chat_id, channel_name):
        try:
            self.cursor.execute("INSERT INTO channels (chat_id, channel_name) VALUES (?, ?)", (chat_id, channel_name))
            self.conn.commit()
        except Exception as e:
            logging.error(f"Ошибка при добавлении канала: {e}")
            raise DatabaseExeption(f"Произошла ошибка при добавлении канала: {e}")

    def get_channel(self, chat_id, channel_name):
        try:
            channel = self.cursor.execute("SELECT * FROM channels WHERE chat_id = ? AND channel_name = ?", (chat_id, channel_name))
            if channel is None:
                return None
            return self.cursor.fetchone()
        except Exception as e:
            logging.error(f"Ошибка при получении канала: {e}")
            raise DatabaseExeption(f"Произошла ошибка при получении канала: {e}")