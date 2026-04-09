def register(bot, db, save_db):
    @bot.message_handler(func=lambda m: m.text.lower() == "готовить")
    def craft_handler(message):
        user_id = str(message.from_user.id)
        user = db["users"][user_id]
        if sum(user["fish"].values()) < 1:
            bot.send_message(message.chat.id, "🐟 Рыбы недостаточно для приготовления!")
            return
        # пример приготовления
        total_fish = sum(user["fish"].values())
        user["dishes"]["рыбное блюдо"] = user["dishes"].get("рыбное блюдо",0)+total_fish
        user["fish"] = {}
        save_db()
        bot.send_message(message.chat.id, f"🍳 Вы приготовили {total_fish} рыбных блюд!")
