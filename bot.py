# bot.py
import telebot
import json
from config import TOKEN
from handlers import fishing, shop, sell, craft, bonus, top, profile, commands
from telebot import types

# ====== Инициализация бота ======
bot = telebot.TeleBot(TOKEN)

# ====== База данных ======
try:
    with open("database/db.json","r") as f:
        db = json.load(f)
except:
    db = {"users":{}, "chats":{}}

def save_db():
    with open("database/db.json","w") as f:
        json.dump(db,f,indent=4)

# ====== Главное меню клавиатуры ======
def main_menu(user_id):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.row("👤 Профиль", "💎 Донат")
    markup.row("🏆 Топы", "🎁 Ежедневный бонус")
    markup.row("📝 Команды")
    return markup

# ====== Сообщение помощи ======
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

БОТ СДЕЛАН НА ЗАКАЗ ДЛЯ @Lisichca1
"""

# ====== Обработчик всех текстовых сообщений ======
@bot.message_handler(func=lambda m: True)
def menu_handler(message):
    text = message.text.lower().strip()
    user_id = str(message.from_user.id)

    # Создаем нового пользователя, если его нет
    if user_id not in db["users"]:
        db["users"][user_id] = {
            "money":0,
            "fish":{},
            "dishes":{},
            "items":{"удочка":1,"приманка":5},
            "last_bonus":0
        }

    # Словарь всех команд
    commands_dict = {
        "команды": lambda m: commands.show_help(m, db, save_db, main_menu(user_id)),
        "помощь": lambda m: commands.show_help(m, db, save_db, main_menu(user_id)),
        "профиль": lambda m: profile.show_profile(m, db, save_db),
        "донат": lambda m: profile.show_donate(m),
        "топы": lambda m: top.show_top_buttons(m),
        "ежедневный бонус": lambda m: bonus.daily_bonus(m, db, save_db),
        "рыбачить": lambda m: fishing.fish_handler(m, db, save_db),
        "магазин": lambda m: shop.shop_handler(m, db, save_db),
        "продать": lambda m: sell.sell_handler(m, db, save_db),
        "готовить": lambda m: craft.craft_handler(m, db, save_db)
    }

    # Выполняем команду, если она есть
    handler = commands_dict.get(text)
    if handler:
        handler(message)
    else:
        bot.send_message(
            message.chat.id,
            "Неизвестная команда. Используйте 📝 Команды",
            reply_markup=main_menu(user_id)
        )

# ====== Приветствие при добавлении бота в чат ======
@bot.message_handler(content_types=["new_chat_members"])
def new_chat(message):
    for user in message.new_chat_members:
        if user.id == bot.get_me().id:
            bot.send_message(
                message.chat.id,
                help_message,
                reply_markup=main_menu(str(message.chat.id))
            )

# ====== Регистрация всех модулей ======
fishing.register(bot, db, save_db)
shop.register(bot, db, save_db)
sell.register(bot, db, save_db)
craft.register(bot, db, save_db)
bonus.register(bot, db, save_db)
top.register(bot, db, save_db)
profile.register(bot, db, save_db)
commands.register(bot, db, save_db)

# ====== Запуск бота ======
if __name__ == "__main__":
    print("Бот запущен...")
    bot.infinity_polling()
