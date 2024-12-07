import logging

from channels.db_channels_functions import db_channels_functions


class Channels_functions():

    def __init__(self, bot):
        self.bot = bot
        self.db = db_channels_functions()

    def get_channels(self, chat_id):
        try:
            self.db.check_channels(chat_id)
        except Exception as e:
            logging.error(f"Ошибка при проверке наличия пользователя: {e}")
            raise Exception(f"Произошла ошибка при проверке наличия пользователя: {e}")

    # TODO Добавить логику проверки уже существующего канала в функцию add_channel
    def add_channel(self, chat_id, channel_name):
        try:
            self.db.add_channel(chat_id, channel_name)
        except Exception as e:
            logging.error(f"Ошибка при добавлении канала: {e}")
            raise Exception(f"Произошла ошибка при добавлении канала: {e}")

    def check_channel(self, chat_id, channel_name):
        try:
            self.db.check_channels(chat_id)
        except Exception as e:
            logging.error(f"Ошибка при проверке наличия канала: {e}")
            raise Exception(f"Произошла ошибка при проверке наличия канала: {e}")