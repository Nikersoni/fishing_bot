import random
from bot import bot, db, save_db

FISH_TYPES = {
    "карп": (1, 5),
    "щука": (2, 6),
    "сом": (3, 8),
    "окунь": (1, 4)
}

def register(bot):

    @bot.message_handler(commands=["collect"])
    @bot.message_handler(func=lambda m: m.text.lower() == "рыбачить")
    def fish_handler(message):
        user_id = str(message.from_user.id)
        if user_id not in db["users"]:
            db["users"][user_id] = {"money":0, "fish":{}, "dishes":{}, "items":{"удочка":1,"приманка":5}, "last_bonus":0}
        
        user = db["users"][user_id]
        # Проверка есть ли удочка и приманка
        if user["items"].get("удочка",0) < 1:
            bot.send_message(message.chat.id, "🎣 У вас нет удочки! Купите в магазине.")
            return
        if user["items"].get("приманка",0) < 1:
            bot.send_message(message.chat.id, "🪱 У вас нет приманки! Купите в магазине.")
            return
        
        # Случайная рыба
        fish = random.choice(list(FISH_TYPES.keys()))
        amount = random.randint(FISH_TYPES[fish][0], FISH_TYPES[fish][1])
        
        # Добавление в инвентарь
        user["fish"][fish] = user["fish"].get(fish,0) + amount
        user["items"]["приманка"] -= 1
        save_db()
        
        bot.send_message(message.chat.id, f"🎣 Вы поймали {amount} шт. {fish}!")
