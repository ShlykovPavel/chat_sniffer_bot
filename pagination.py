from telebot import types

def get_paginated_channels(channels, page, items_per_page=10):
    """
    Формирует список каналов для отображения на заданной странице.
    """
    start_index = page * items_per_page
    end_index = start_index + items_per_page
    page_channels = channels[start_index:end_index]

    total_pages = (len(channels) - 1) // items_per_page + 1
    return page_channels, total_pages

def create_pagination_keyboard(page_channels, page, total_pages):
    # Создаем Inline клавиатуру
    markup = types.InlineKeyboardMarkup()

    for channel in page_channels:
        button = types.InlineKeyboardButton(channel, callback_data=f"remove_channel:{channel}")
        markup.add(button)

    # Добавляем кнопки "Назад" и "Вперед"
    navigation_row = []
    if page > 0:
        navigation_row.append(types.InlineKeyboardButton("⬅ Назад", callback_data=f"channels_page:{page - 1}"))
    if page < total_pages - 1:
        navigation_row.append(types.InlineKeyboardButton("Вперед ➡", callback_data=f"channels_page:{page + 1}"))

    if navigation_row:
        markup.row(*navigation_row)