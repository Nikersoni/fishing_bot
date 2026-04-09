def register(bot, db, save_db):
    @bot.message_handler(func=lambda m: m.text.lower() in ["команды","помощь"])
    def show_help(message, db=db, save_db=save_db, markup=None):
        text = """Список всех команд:

👤 Профиль  
💎 Донат  
🏆 Топы  
🎁 Ежедневный бонус  
🎣 Рыбачить  
💰 Продать  
🛒 Магазин  
🍳 Готовить  
📝 Команды"""
        bot.send_message(message.chat.id, text, reply_markup=markup)
