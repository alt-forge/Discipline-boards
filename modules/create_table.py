import os

async def create(update, context):
    User_ID = str(update.message.from_user.id)
    text = update.message.text
    
    os.makedirs(f"data/{User_ID}/table-txt", exist_ok=True)

    file_path = f"data/{User_ID}/table-txt/{text}.txt"

    if not os.path.exists(file_path):
        with open(file_path, "w") as file:
            file.write("W")
        await update.message.reply_text(f"Таблица '{text}' успешно создана!")
        context.user_data["waiting_table_create"] = False
    else:
        await update.message.reply_text(
            f"Таблица '{text}' уже существует. Пожалуйста, выберите другое имя."
        )
    