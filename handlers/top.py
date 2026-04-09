from telebot import types

def register(bot, db, save_db):
    @bot.message_handler(func=lambda m: m.text.lower() == "топы")
    def show_top_buttons(message):
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton("🐟 Рыба", callback_data="top_fish"))
        markup.add(types.InlineKeyboardButton("💰 Деньги", callback_data="top_money"))
        markup.add(types.InlineKeyboardButton("🍳 Блюда", callback_data="top_dishes"))
        markup.add(types.InlineKeyboardButton("🏛 Чаты", callback_data="top_chats"))
        bot.send_message(message.chat.id, "Выберите топ:", reply_markup=markup)

    @bot.callback_query_handler(func=lambda c: c.data.startswith("top_"))
    def top_callback(call):
        text = ""
        if call.data=="top_fish":
            text = "🐟 Топ по рыбе"
        elif call.data=="top_money":
            text = "💰 Топ по деньгам"
        elif call.data=="top_dishes":
            text = "🍳 Топ по блюдам"
        elif call.data=="top_chats":
            text = "🏛 Топ чатов"
        bot.send_message(call.message.chat.id, text)
