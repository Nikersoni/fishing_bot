from telebot import types
from bot import bot, db, save_db

SHOP_ITEMS = {
    "удочка": 500,
    "приманка": 50
}

def register(bot):

    @bot.message_handler(commands=["shop"])
    @bot.message_handler(func=lambda m: m.text.lower() == "магазин")
    def shop_handler(message):
        user_id = str(message.from_user.id)
        if user_id not in db["users"]:
            db["users"][user_id] = {"money":0, "fish":{}, "dishes":{}, "items":{}, "last_bonus":0}
        
        markup = types.InlineKeyboardMarkup()
        for item, price in SHOP_ITEMS.items():
            markup.add(types.InlineKeyboardButton(f"{item} - {price}💰", callback_data=f"buy_{item}"))
        bot.send_message(message.chat.id, "🛒 Магазин:", reply_markup=markup)

    @bot.callback_query_handler(func=lambda call: call.data.startswith("buy_"))
    def buy_item(call):
        item = call.data[4:]
        user_id = str(call.from_user.id)
        user = db["users"][user_id]
        price = SHOP_ITEMS[item]
        if user["money"] >= price:
            user["money"] -= price
            user["items"][item] = user["items"].get(item,0)+1
            save_db()
            bot.send_message(call.message.chat.id, f"✅ Вы купили {item} за {price}💰")
        else:
            bot.send_message(call.message.chat.id, "❌ Недостаточно монет")
