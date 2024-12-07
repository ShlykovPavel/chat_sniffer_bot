import logging

from users.db_user_functions import db_user_functions


class users_functions():
    def __init__(self, bot):
        self.db = db_user_functions()
        self.bot = bot

    def start_registration(self, chat_id, user_name_to_register):
        try:
            # Сохраняем пользователя в базу данных
            self.db.add_user(chat_id=chat_id, username=user_name_to_register)
            self.bot.send_message(chat_id,
                                  f"Привет! Я бот для мониторинга вакансий и заказов из публичных групп по ключевым словам. Список моих команд - /cmd_list")
        except Exception as e:
            logging.error(f"Ошибка регистрации: {e}")
            self.bot.send_message(chat_id, "Произошла ошибка при регистрации. Попробуйте позже.")

    def check_users(self, chat_id):
        try:
            self.db.check_users(chat_id)
        except Exception as e:
            logging.error(f"Ошибка при проверке наличия пользователя: {e}")
            raise Exception(f"Произошла ошибка при проверке наличия пользователя: {e}")
