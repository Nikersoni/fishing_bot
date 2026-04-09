from bot import bot, db, save_db

CRAFT_RECIPES = {
    "карп": "карп жареный",
    "щука": "щука жареная",
    "сом": "сом жареный",
    "окунь": "окунь жареный"
}

def register(bot):

    @bot.message_handler(commands=["craft"])
    @bot.message_handler(func=lambda m: m.text.lower() == "готовить")
    def craft_handler(message):
        user_id = str(message.from_user.id)
        user = db["users"][user_id]

        fish_list = [f for f in user["fish"] if user["fish"][f]>0]
        if not fish_list:
            bot.send_message(message.chat.id, "❌ У вас нет рыбы для приготовления")
            return

        # Берём первую рыбу из списка
        fish = fish_list[0]
        dish = CRAFT_RECIPES[fish]

        user["fish"][fish] -= 1
        user["dishes"][dish] = user["dishes"].get(dish,0)+1
        save_db()
        bot.send_message(message.chat.id, f"🍳 Вы приготовили: {dish}!")
