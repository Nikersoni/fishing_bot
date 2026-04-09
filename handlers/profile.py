from telebot import types

def register(bot, db, save_db):

    @bot.message_handler(commands=["profile"])
    def profile_handler(message):
        user_id = str(message.from_user.id)
        if user_id not in db["users"]:
            db["users"][user_id] = {"money":0, "fish":0, "dishes":0, "last_bonus":0}
            save_db()
        user = db["users"][user_id]
        text = (f"👤 Профиль:\n\n"
                f"💰 Деньги: {user['money']}\n"
                f"🎣 Рыба поймана: {user['fish']}\n"
                f"🍳 Приготовлено блюд: {user['dishes']}")
        bot.send_message(message.chat.id, text)
