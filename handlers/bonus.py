import time
from config import BONUS_AMOUNT, BONUS_COOLDOWN

def register(bot, db, save_db):

    @bot.message_handler(commands=["daily"])
    def daily_bonus(message):
        user_id = str(message.from_user.id)
        now = time.time()
        if user_id not in db["users"]:
            db["users"][user_id] = {"money":0, "fish":0, "dishes":0, "last_bonus":0}
        last = db["users"][user_id].get("last_bonus", 0)

        if now - last >= BONUS_COOLDOWN:
            db["users"][user_id]["money"] += BONUS_AMOUNT
            db["users"][user_id]["last_bonus"] = now
            save_db()
            bot.send_message(message.chat.id, f"🎁 Вы получили ежедневный бонус!\n💰 +{BONUS_AMOUNT} монет\n⏰ Следующий бонус через 24 часа")
        else:
            remaining = int(BONUS_COOLDOWN - (now - last))
            hours = remaining//3600
            minutes = (remaining%3600)//60
            seconds = remaining%60
            bot.send_message(message.chat.id, f"⏰ Бонус уже получен!\nСледующий бонус через: {hours:02}:{minutes:02}:{seconds:02}")
