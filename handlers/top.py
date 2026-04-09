from telebot import types

def register(bot, db):

    @bot.message_handler(commands=["top"])
    def top_handler(message):
        markup = types.InlineKeyboardMarkup()
        markup.row(
            types.InlineKeyboardButton("🐟 Рыба", callback_data="top_fish"),
            types.InlineKeyboardButton("👑 Деньги", callback_data="top_money")
        )
        markup.row(
            types.InlineKeyboardButton("🍳 Блюда", callback_data="top_dishes"),
            types.InlineKeyboardButton("💬 Чаты", callback_data="top_chats")
        )
        bot.send_message(message.chat.id, "Выберите интересующий топ:", reply_markup=markup)

    @bot.callback_query_handler(func=lambda call: call.data.startswith("top_"))
    def callback_top(call):
        cat = call.data.split("_")[1]
        text = ""
        if cat == "fish":
            text = "🏆 Топ рыбаков:\n1. @Nextriz — 45 рыб\n2. @FisherMan — 42 рыб\n3. @Karasik — 38 рыб"
        elif cat == "money":
            text = "🏆 Топ по монетам:\n1. @RichFish — 5400 💰\n2. @GoldHook — 4300 💰\n3. @Nextriz — 3200 💰"
        elif cat == "dishes":
            text = "🏆 Топ поваров:\n1. @ChefFish — 15 блюд\n2. @Nextriz — 12 блюд\n3. @CookHook — 10 блюд"
        elif cat == "chats":
            text = "🏆 Топ чатов:\n1. РыбакиPRO — 15000 💰\n2. HookMasters — 12000 💰\n3. FishTown — 8500 💰"
        bot.send_message(call.message.chat.id, text)
