import time
from config import BONUS_AMOUNT, BONUS_COOLDOWN

def register(bot, db, save_db):
    @bot.message_handler(func=lambda m: m.text.lower() in ["ежедневный бонус","бонус"])
    def daily_bonus(message):
        user_id = str(message.from_user.id)
        user = db["users"][user_id]
        now = int(time.time())
        if now - user.get("last_bonus",0) < BONUS_COOLDOWN:
            next_bonus = BONUS_COOLDOWN - (now - user.get("last_bonus",0))
            hours = next_bonus//3600
            minutes = (next_bonus%3600)//60
            seconds = next_bonus%60
            bot.send_message(message.chat.id,f"⏱ Вы уже получили бонус. Следующий через {hours}ч {minutes}м {seconds}с")
            return
        user["money"] += BONUS_AMOUNT
        user["last_bonus"] = now
        save_db()
        bot.send_message(message.chat.id,f"🎁 Вы получили {BONUS_AMOUNT}💰!")
