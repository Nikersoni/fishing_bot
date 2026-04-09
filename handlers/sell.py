def register(bot, db, save_db):
    @bot.message_handler(func=lambda m: m.text.lower() == "продать")
    def sell_handler(message):
        user_id = str(message.from_user.id)
        user = db["users"][user_id]
        total_money = 0
        for fish, amount in user["fish"].items():
            total_money += amount*10  # цена 1 рыбки = 10
        user["money"] += total_money
        user["fish"] = {}
        save_db()
        bot.send_message(message.chat.id, f"💰 Вы продали всю рыбу за {total_money}💰")
