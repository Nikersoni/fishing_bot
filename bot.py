import telebot
from telebot import types
import sqlite3
import random
import os

TOKEN = os.getenv("8660641414:AAEgmiRuWFa0ftw4_Is7pcy30E9LjwZxY9c")  # для хостинга
CHANNEL = "@LeBomjara"   # замени на свой канал

bot = telebot.TeleBot(TOKEN)

# --- БД ---
conn = sqlite3.connect('users.db', check_same_thread=False)
cursor = conn.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS users (
    user_id INTEGER PRIMARY KEY,
    balance REAL DEFAULT 0,
    referrer_id INTEGER,
    ref_count INTEGER DEFAULT 0,
    is_activated INTEGER DEFAULT 0
)
''')
conn.commit()

# --- КАПЧА ---
captcha_data = {}

# --- КЛАВИАТУРА ---
def main_keyboard():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add("👤 Профиль")
    markup.add("🎁 Бонус")
    markup.add("📰 Новости")
    markup.add("🏆 Топ")
    return markup

def subscribe_keyboard():
    markup = types.InlineKeyboardMarkup()

    sub_btn = types.InlineKeyboardButton(
        "📢 Подписаться",
        url=f"https://t.me/{CHANNEL.replace('@','')}"
    )

    check_btn = types.InlineKeyboardButton(
        "✅ Проверить",
        callback_data="check_sub"
    )

    markup.add(sub_btn)
    markup.add(check_btn)
    return markup

# --- ФУНКЦИИ ---
def add_user(user_id, referrer_id=None):
    cursor.execute("SELECT * FROM users WHERE user_id = ?", (user_id,))
    if cursor.fetchone() is None:
        cursor.execute(
            "INSERT INTO users (user_id, referrer_id) VALUES (?, ?)",
            (user_id, referrer_id)
        )
        conn.commit()

def get_balance(user_id):
    cursor.execute("SELECT balance FROM users WHERE user_id = ?", (user_id,))
    result = cursor.fetchone()
    return result[0] if result else 0

def is_subscribed(user_id):
    try:
        member = bot.get_chat_member(CHANNEL, user_id)
        return member.status in ['member', 'creator', 'administrator']
    except:
        return False

def generate_captcha(user_id):
    a = random.randint(1, 10)
    b = random.randint(1, 10)
    captcha_data[user_id] = a + b
    return f"🧠 Реши пример:\n\n{a} + {b} = ?"

def activate_user(user_id):
    cursor.execute("SELECT is_activated, referrer_id FROM users WHERE user_id = ?", (user_id,))
    result = cursor.fetchone()

    if not result:
        return

    is_activated, referrer_id = result

    if is_activated == 1:
        return

    cursor.execute("UPDATE users SET is_activated = 1 WHERE user_id = ?", (user_id,))

    if referrer_id and referrer_id != user_id:
        cursor.execute(
            "UPDATE users SET balance = balance + 2.5, ref_count = ref_count + 1 WHERE user_id = ?",
            (referrer_id,)
        )

    conn.commit()

def get_top_users():
    cursor.execute(
        "SELECT user_id, ref_count FROM users ORDER BY ref_count DESC LIMIT 10"
    )
    return cursor.fetchall()

def get_user_rank(user_id):
    cursor.execute("""
        SELECT COUNT(*) + 1 FROM users 
        WHERE ref_count > (SELECT ref_count FROM users WHERE user_id = ?)
    """, (user_id,))
    return cursor.fetchone()[0]

# --- START ---
@bot.message_handler(commands=['start'])
def start(message):
    args = message.text.split()

    referrer_id = None
    if len(args) > 1:
        try:
            referrer_id = int(args[1])
        except:
            pass

    add_user(message.from_user.id, referrer_id)

    bot.send_message(
        message.chat.id,
        "💸 Зарабатывай в Telegram!\n\n"
        "+2.5$ за каждого друга 👇",
        reply_markup=main_keyboard()
    )

# --- ПРОФИЛЬ ---
@bot.message_handler(func=lambda m: m.text == "👤 Профиль")
def profile(message):
    user_id = message.from_user.id
    balance = get_balance(user_id)

    ref_link = f"https://t.me/{bot.get_me().username}?start={user_id}"

    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton(
        "📤 Пригласить друга",
        url=f"https://t.me/share/url?url={ref_link}"
    ))

    bot.send_message(
        message.chat.id,
        f"👤 Профиль\n\n"
        f"💰 Баланс: {balance}$\n\n"
        f"🔗 <a href='{ref_link}'>Ссылка для рефералов</a>\n\n"
        f"📩 Приглашай друзей и получай +2.5$",
        reply_markup=markup,
        parse_mode="HTML"
    )

# --- БОНУС ---
@bot.message_handler(func=lambda m: m.text == "🎁 Бонус")
def bonus(message):
    user_id = message.from_user.id

    if not is_subscribed(user_id):
        bot.send_message(
            message.chat.id,
            "❌ Подпишись на канал!",
            reply_markup=subscribe_keyboard()
        )
        return

    bot.send_message(message.chat.id, generate_captcha(user_id))

# --- ПРОВЕРКА ПОДПИСКИ ---
@bot.callback_query_handler(func=lambda call: call.data == "check_sub")
def check_sub(call):
    user_id = call.from_user.id

    if is_subscribed(user_id):
        bot.answer_callback_query(call.id, "Подписка есть!")
        bot.send_message(call.message.chat.id, generate_captcha(user_id))
    else:
        bot.answer_callback_query(call.id, "Ты не подписан 😢", show_alert=True)

# --- КАПЧА ---
@bot.message_handler(func=lambda message: message.from_user.id in captcha_data)
def check_captcha(message):
    user_id = message.from_user.id

    try:
        answer = int(message.text)
    except:
        bot.send_message(message.chat.id, "❌ Введи число")
        return

    if captcha_data[user_id] == answer:
        del captcha_data[user_id]
        activate_user(user_id)

        bot.send_message(
            message.chat.id,
            "✅ Бонус активирован 💰",
            reply_markup=main_keyboard()
        )
    else:
        bot.send_message(message.chat.id, "❌ Неверно!\n\n" + generate_captcha(user_id))

# --- ТОП ---
@bot.message_handler(func=lambda m: m.text == "🏆 Топ")
def top_users(message):
    top = get_top_users()
    user_id = message.from_user.id

    text = "🏆 ТОП по рефералам:\n\n"
    medals = ["🥇", "🥈", "🥉"]

    for i, user in enumerate(top, start=1):
        uid, ref_count = user

        try:
            user_info = bot.get_chat(uid)
            name = f"@{user_info.username}" if user_info.username else user_info.first_name
        except:
            name = f"ID {uid}"

        medal = medals[i-1] if i <= 3 else f"{i}."
        text += f"{medal} {name} — {ref_count} реф.\n"

    rank = get_user_rank(user_id)
    text += f"\n📍 Ты на {rank} месте"

    bot.send_message(message.chat.id, text)

# --- НОВОСТИ ---
@bot.message_handler(func=lambda m: m.text == "📰 Новости")
def news(message):
    bot.send_message(
        message.chat.id,
        "📰 Новости:\n\nСкоро обновления 🚀",
        reply_markup=main_keyboard()
    )

# --- ЗАПУСК ---
print("Бот запущен...")
bot.polling(none_stop=True)
