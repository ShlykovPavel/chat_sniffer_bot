import logging

from telebot import types

from channels.channels_functions import Channels_functions
from db.database import Database
from users.users_functions import users_functions
from pagination import *

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,  # Уровень логов (DEBUG, INFO, WARNING, ERROR, CRITICAL)
    format='%(asctime)s - %(levelname)s - %(message)s',  # Формат логов
    handlers=[logging.StreamHandler()]  # Поток вывода (можно указать файл)
)


class Bot_commands:
    def __init__(self, bot, user_data):
        self.bot = bot
        self.db = Database()
        self.user_data = user_data
        self.user_functions = users_functions(self.bot)
        self.channels_functions = Channels_functions(self.bot)

    def register_handlers(self):
        # Обработчик команды /start
        @self.bot.message_handler(commands=['start'])
        def start_registration(message):
            chat_id = message.chat.id
            username = message.from_user.username
            if self.user_functions.check_users(chat_id):
                self.bot.send_message(chat_id, "Вы уже зарегистрированы.")
            else:
                self.user_functions.start_registration(chat_id, username)

        @self.bot.message_handler(commands=['cmd_list'])
        def send_command_list(message):
            chat_id = message.chat.id
            command_list = [
                '/cmd_list - список команд',
                '/channel_list - ваш список чатов/каналов для мониторинга',
                '/add_channel (username канала) - добавить в список чат/канал для мониторинга',
                '/remove_channel (username канала) - убрать из списка чат/канал для мониторинга',
                '/keyword_list - список ключевых слов, о сообщениях с которыми бот будет уведомлять',
                '/add_keyword (ключевое слово) - добавить в список ключевое слово',
                '/remove_keyword (ключевое слово) - убрать из списка ключевое слово',
                'Со мной ты самый первый будешь откликаться на интересующие тебя вакансии и заказы!'
            ]
            self.bot.send_message(chat_id, '\n'.join(command_list))

        # @self.bot.message_handler(commands=['channel_list'])
        # def show_channels(message):
        #     chat_id = message.chat.id
        #     channels = self.channels_functions.get_channels(chat_id)
        #     if not channels:
        #         self.bot.send_message(chat_id, "У вас нет чатов/каналов для мониторинга.")
        #         return
        #     markup = types.InlineKeyboardMarkup()
        #     for channel in channels:
        #         button = types.InlineKeyboardButton(channel, callback_data=f"remove_channel:{channel}")
        #         markup.add(button)
        #     self.bot.send_message(chat_id, "Список чатов/каналов для мониторинга:", reply_markup=markup)

        @self.bot.message_handler(commands=['channel_list'])
        def show_channels(message):
            chat_id = message.chat.id
            channels = self.channels_functions.get_channels(chat_id)
            if not channels:
                self.bot.send_message(chat_id, "Нет чатов/каналов для мониторинга.")
                return

            page = 0
            page_channels, total_pages = get_paginated_channels(channels, page)

            markup = types.InlineKeyboardMarkup()

            for channel in page_channels:
                # Преобразуем channel в строку
                channel_name = channel[0]
                button = types.InlineKeyboardButton(channel_name, callback_data=f"remove_channel:{channel_name}")
                markup.add(button)

            # Добавляем кнопки "Назад" и "Вперед"
            navigation_row = []
            if page > 0:
                navigation_row.append(types.InlineKeyboardButton("⬅ Назад", callback_data=f"channels_page:{page - 1}"))
            if page < total_pages - 1:
                navigation_row.append(types.InlineKeyboardButton("Вперед ➡", callback_data=f"channels_page:{page + 1}"))

            if navigation_row:
                markup.row(*navigation_row)

            # Отправляем сообщение с пагинацией
            self.bot.send_message(chat_id, f"Страница {page + 1} из {total_pages}:", reply_markup=markup)

        @self.bot.callback_query_handler(func=lambda call: call.data.startswith('channels_page:'))
        def handle_channels_pagination(call):
            chat_id = call.message.chat.id
            page = int(call.data.split(':')[1])  # Извлекаем номер страницы из callback_data
            channels = self.channels_functions.get_channels(chat_id)

            # Получаем данные для указанной страницы
            page_channels, total_pages = get_paginated_channels(channels, page)

            # Создаем клавиатуру для указанной страницы
            markup = types.InlineKeyboardMarkup()

            for channel in page_channels:
                # Преобразуем channel в строку
                channel_name = channel[0]
                button = types.InlineKeyboardButton(channel_name, callback_data=f"remove_channel:{channel_name}")
                markup.add(button)

            # Добавляем кнопки "Назад" и "Вперед"
            navigation_row = []
            if page > 0:
                navigation_row.append(types.InlineKeyboardButton("⬅ Назад", callback_data=f"channels_page:{page - 1}"))
            if page < total_pages - 1:
                navigation_row.append(types.InlineKeyboardButton("Вперед ➡", callback_data=f"channels_page:{page + 1}"))

            if navigation_row:
                markup.row(*navigation_row)

            # Обновляем сообщение с новой страницей
            self.bot.edit_message_text(
                chat_id=chat_id,
                message_id=call.message.message_id,
                text=f"Страница {page + 1} из {total_pages}:",
                reply_markup=markup
            )

        @self.bot.message_handler(commands=['add_channel'])
        def add_channel(message):
            chat_id = message.chat.id
            try:
                self.bot.send_message(chat_id, "Введите username канала:")
                self.bot.register_next_step_handler(message, lambda msg: self.channels_functions.add_channel(chat_id, msg.text))
            except Exception as e:
                logging.error(f"Ошибка при добавлении канала: {e}")
                self.bot.send_message(chat_id, f"Произошла ошибка при добавлении канала: {e}")

