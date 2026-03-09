from telegram import Update, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, MessageHandler, filters
from config import BOT_TOKEN
import os, shutil

import modules.create_table as create_table
import modules.get_tables as get_tables 
import modules.set_table as set_table
import modules.view_table as view_table
import modules.delete_table as delete_table
import modules.analytics as analytics


menu_buttons_main = [
    [KeyboardButton("Создать таблицу")],
    [KeyboardButton("Создать отметку")],
    [KeyboardButton("Посмотреть таблицу")],
    [KeyboardButton("Удалить таблицу")],
    [KeyboardButton("Сброс профиля")]
]

menu_buttons_color = [
    [KeyboardButton("🔴")],
    [KeyboardButton("🟡")],
    [KeyboardButton("🟢")]
]

menu_markup_main = ReplyKeyboardMarkup(menu_buttons_main, resize_keyboard=True)
menu_markup_color = ReplyKeyboardMarkup(menu_buttons_color, resize_keyboard=True)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Привет! Я твой бот для отслеживания дисциплины. Выбери действие из меню ниже:",
        reply_markup=menu_markup_main
    )


async def handle_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    user_id = update.message.from_user.id
    keyboard_tables = get_tables.get_tables_keyboard(user_id)

# Создание таблицы
    if text == "Создать таблицу":
        context.user_data["waiting_table_create"] = True
        await update.message.reply_text("Введите название таблицы:")

    elif context.user_data.get("waiting_table_create"):
        await create_table.create(update, context)

# Создание отметки
    elif text == "Создать отметку":
        if len(keyboard_tables.keyboard) == 0:
            await update.message.reply_text("У вас нет таблиц для создания отметки.")
        else:
            await update.message.reply_text(
                "Выберите таблицу:",
                reply_markup=keyboard_tables
            )

            context.user_data["waiting_table_set_table"] = True

    elif context.user_data.get("waiting_table_set_table"):
        context.user_data["waiting_table_set_table"] = False
        context.user_data["selected_table"] = text

        await update.message.reply_text(
            "Вы выбрали таблицу. Теперь выберите отметку:",
            reply_markup=menu_markup_color
        )

        context.user_data["waiting_table_set_color"] = True

    elif context.user_data.get("waiting_table_set_color"):
        set_table.set_table(update, context)
        await update.message.reply_text("Отметка успешно обновлена!", reply_markup=menu_markup_main)


# Просмотр таблиц
    elif text == "Посмотреть таблицу":
        if len(keyboard_tables.keyboard) == 0:
            await update.message.reply_text("У вас нет таблиц для просмотра.")
        else:
            await update.message.reply_text(
                "Выберите таблицу:",
                reply_markup=keyboard_tables
            )

            context.user_data["waiting_table_view"] = True

    elif context.user_data.get("waiting_table_view"):
        context.user_data["waiting_table_view"] = False
        context.user_data["selected_table"] = text

        table_name = context.user_data.get("selected_table")

        file_path_txt = f"data/{user_id}/table-txt/{table_name}.txt"
        file_path_png = f"data/{user_id}/table-png/{table_name}.png"

        if not os.path.exists(f"data/{user_id}/table-png"):
            os.mkdir(f"data/{user_id}/table-png")

        view_table.view_table(file_path_txt, file_path_png)
        await update.message.reply_photo(photo=open(file_path_png, 'rb'), caption=analytics.analytics(file_path_txt), reply_markup=menu_markup_main)

# Удаление таблицы
    elif text == "Удалить таблицу":
        if len(keyboard_tables.keyboard) == 0:
            await update.message.reply_text("У вас нет таблиц для удаления.")
        else:
            await update.message.reply_text(
                "Выберите таблицу для удаления:",
                reply_markup=keyboard_tables
            )

            context.user_data["waiting_table_delete"] = True

    elif context.user_data.get("waiting_table_delete"):
        context.user_data["waiting_table_delete"] = False
        context.user_data["selected_table"] = text

        table_name = context.user_data.get("selected_table")

        file_path_txt = f"data/{user_id}/table-txt/{table_name}.txt"
        file_path_png = f"data/{user_id}/table-png/{table_name}.png"

        delete_table.delete_table(file_path_txt, file_path_png)
        await update.message.reply_text(f"Таблица '{table_name}' успешно удалена!", reply_markup=menu_markup_main)


# Сброс профиля
    elif text == "Сброс профиля":
        file_path = f"data/{user_id}"
        if os.path.exists(file_path):
            shutil.rmtree(file_path)
            await update.message.reply_text("Профиль успешно сброшен.", reply_markup=menu_markup_main)
        else:
            await update.message.reply_text("Профиля нет.", reply_markup=menu_markup_main)

    else:
        await update.message.reply_text("Выбери действие из меню.")


if __name__ == "__main__":
    TOKEN = BOT_TOKEN

    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_menu))

    print("Бот запущен...")

    app.run_polling()