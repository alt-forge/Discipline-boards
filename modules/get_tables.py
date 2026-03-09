import os
from telegram import ReplyKeyboardMarkup, KeyboardButton

def get_tables_keyboard(user_id):
    path = f"data/{user_id}/table-txt"

    if not os.path.exists(path):
        return ReplyKeyboardMarkup([[KeyboardButton("Нет таблиц")]], resize_keyboard=True)

    files = os.listdir(path)

    menu_buttons2 = []

    for file in files:
        if file.endswith(".txt"):
            table_name = file[:-4]
            menu_buttons2.append([KeyboardButton(table_name)])

    return ReplyKeyboardMarkup(menu_buttons2, resize_keyboard=True)