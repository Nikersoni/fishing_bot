import random

FISH_TYPES = {
    "карп": (1, 5),
    "щука": (2, 6),
    "сом": (3, 8),
    "окунь": (1, 4)
}

def register(bot, db, save_db):
    @bot.message_handler(commands=["collect"])
    @bot.message_handler(func=lambda m: m.text.lower() == "рыбачить")
    def fish_handler(message):
        user_id = str(message.from_user.id)
        if user_id not in db["users"]:
            db["users"][user_id] = {"money":0, "fish":{}, "dishes":{}, "items":{"удочка":1,"приманка":5}, "last_bonus":0}

        user = db["users"][user_id]
        if user["items"].get("удочка",0) < 1:
            bot.send_message(message.chat.id, "🎣 У вас нет удочки!")
            return
        if user["items"].get("приманка",0) < 1:
            bot.send_message(message.chat.id, "🪱 У вас нет приманки!")
            return

        fish = random.choice(list(FISH_TYPES.keys()))
        amount = random.randint(FISH_TYPES[fish][0], FISH_TYPES[fish][1])
        user["fish"][fish] = user["fish"].get(fish,0) + amount
        user["items"]["приманка"] -= 1
        save_db()
        bot.send_message(message.chat.id, f"🎣 Вы поймали {amount} шт. {fish}!")
