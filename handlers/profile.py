def register(bot, db, save_db):
    @bot.message_handler(func=lambda m: m.text.lower() == "профиль")
    def show_profile(message, db=db, save_db=save_db):
        user_id = str(message.from_user.id)
        user = db["users"][user_id]
        fish_count = sum(user["fish"].values())
        dishes_count = sum(user["dishes"].values())
        money = user["money"]
        bot.send_message(message.chat.id, f"👤 Профиль:\n💰 Деньги: {money}\n🐟 Рыба: {fish_count}\n🍳 Блюда: {dishes_count}")

    @bot.message_handler(func=lambda m: m.text.lower() == "донат")
    def show_donate(message):
        bot.send_message(message.chat.id,"💎 Донат пока что отсутствует, но можно добавить через платежный API")
