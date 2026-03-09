import os

def set_table(update, context):
    mark = update.message.text
    table = context.user_data.get("selected_table")
    user_id = update.message.from_user.id

    path = f"data/{user_id}/table-txt/{table}.txt"

    with open(path, "r") as file:
        data = file.read()

    if data[-1] == "W":

        if mark == "🔴":
            new = "R"
        elif mark == "🟡":
            new = "Y"
        elif mark == "🟢":
            new = "G"
        else:
            return

        with open(path, "w") as file:
            file.write(data[:-1] + new + "W")


    context.user_data["waiting_table_set_color"] = False 
    