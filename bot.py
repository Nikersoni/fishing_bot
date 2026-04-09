import telebot
from config import TOKEN
import json
from handlers import commands, bonus, top, profile, fishing, shop, sell, craft
from telebot import types

bot = telebot.TeleBot(TOKEN)

# --- Загрузка базы ---
try:
    with open("database/db.json", "r") as f:
        db = json.load(f)
except:
    db = {"users": {}, "chats": {}}

def save_db():
    with open("database/db.json", "w") as f:
        json.dump(db, f, indent=4)

# --- Сообщение помощи ---
help_message = """Привет! 👋

Вот список всех команд бота:

👤 Баланс — /balance или Баланс  
🎁 Ежедневный бонус — /daily или Бонус / Ежедневный бонус  
🏆 Топы — /top или Топ (выбор через инлайн-кнопки: Рыба, Деньги, Блюда, Чаты)  
💎 Донат — /donate или Донат  
👤 Профиль — /profile или Профиль  
📝 Команды — /commands или Команды  
🏛 Казна чата — /kazna или Казна (только в группах)  
🎣 Рыбачить — /collect или Рыбачить  
💰 Продать — /sell или Продать  
🛒 Магазин — /shop или Магазин  
🎒 Инвентарь — /inventory или Инвентарь  
🍳 Готовить — /craft или Готовить
"""

# --- Главное меню клавиатуры ---
def main_menu(user_id):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.row("👤 Профиль", "💎 Донат")
    markup.row("🏆 Топы", "🎁 Ежедневный бонус")
    markup.row("📝 Команды")
    return markup

# --- Обработчик клавиатуры ---
@bot.message_handler(func=lambda m: True)
def menu_handler(message):
    text = message.text.lower()
    user_id = str(message.from_user.id)

    if user_id not in db["users"]:
        db["users"][user_id] = {"money":0, "fish":{}, "dishes":{}, "items":{"удочка":1,"приманка":5}, "last_bonus":0}
    
    if text in ["команды", "помощь"]:
        bot.send_message(message.chat.id, help_message, reply_markup=main_menu(user_id))
    elif text == "профиль":
        bot.send_message(message.chat.id, "Вы открыли профиль:", reply_markup=main_menu(user_id))
        profile.show_profile(message, db, save_db)
    elif text == "донат":
        bot.send_message(message.chat.id, "💎 Донат: Вы можете пополнить монеты через систему доната.", reply_markup=main_menu(user_id))
    elif text == "топы":
        bot.send_message(message.chat.id, "Выберите топ:", reply_markup=main_menu(user_id))
        top.show_top_buttons(message)
    elif text == "ежедневный бонус":
        bonus.daily_bonus(message, db, save_db)
    elif text in ["рыбачить", "магазин", "продать", "готовить"]:
        # вызываем соответствующие игровые модули
        if text == "рыбачить":
            fishing.fish_handler(message, db, save_db)
        elif text == "магазин":
            shop.shop_handler(message, db, save_db)
        elif text == "продать":
            sell.sell_handler(message, db, save_db)
        elif text == "готовить":
            craft.craft_handler(message, db, save_db)
    else:
        bot.send_message(message.chat.id, "Неизвестная команда. Используйте 📝 Команды", reply_markup=main_menu(user_id))

# --- Приветствие при добавлении бота ---
@bot.message_handler(content_types=["new_chat_members"])
def new_chat(message):
    for user in message.new_chat_members:
        if user.id == bot.get_me().id:
            bot.send_message(message.chat.id, help_message, reply_markup=main_menu(str(message.chat.id)))

# --- Подключение модулей слеш-команд ---
commands.register(bot, db, save_db, help_message)
bonus.register(bot, db, save_db)
top.register(bot, db)
profile.register(bot, db, save_db)
fishing.register(bot)
shop.register(bot)
sell.register(bot)
craft.register(bot)

# --- Запуск ---
print("Бот запущен...")
bot.infinity_polling()
