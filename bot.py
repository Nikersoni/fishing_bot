import telebot
from config import TOKEN
import json
from handlers import commands, bonus, top, profile

# --- Инициализация бота ---
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

Используй команды через слеш `/` или текст.
В личке бонус доступен через кнопку 🎁 Ежедневный бонус.
"""

# --- Триггеры текста ---
@bot.message_handler(func=lambda message: message.text.lower() in ["команды", "помощь"])
def send_help(message):
    bot.send_message(message.chat.id, help_message)

# --- Приветствие при добавлении бота в чат ---
@bot.message_handler(content_types=["new_chat_members"])
def new_chat(message):
    for user in message.new_chat_members:
        if user.id == bot.get_me().id:
            bot.send_message(message.chat.id, help_message)

# --- Подключение модулей ---
commands.register(bot, db, save_db, help_message)
bonus.register(bot, db, save_db)
top.register(bot, db)
profile.register(bot, db, save_db)

# --- Запуск бота ---
print("Бот запущен...")
bot.infinity_polling()
