from telebot import types
from bot import bot, db, save_db

SELL_PRICES = {
    "карп": 50,
    "щука": 70,
    "сом": 100,
    "окунь": 40
}

def register(bot):

    @bot.message_handler(commands=["sell"])
    @bot.message_handler(func=lambda m: m.text.lower() == "продать")
    def sell_handler(message):
        user_id = str(message.from_user.id)
        user = db["users"][user_id]

        fish_list = [f for f in user["fish"] if user["fish"][f]>0]
        if not fish_list:
            bot.send_message(message.chat.id, "❌ У вас нет рыбы для продажи")
            return
        
        total = 0
        text = "💰 Вы продали:\n"
        for f in fish_list:
            amount = user["fish"][f]
            price = SELL_PRICES[f] * amount
            total += price
            text += f"{f} x{amount} = {price}💰\n"
            user["fish"][f] = 0
        
        user["money"] += total
        save_db()
        bot.send_message(message.chat.id, text+f"Итого: {total}💰")
