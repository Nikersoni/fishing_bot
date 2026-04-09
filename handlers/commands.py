from telebot import types

def register(bot, db, save_db, help_message):

    @bot.message_handler(commands=["commands", "help"])
    def commands_handler(message):
        bot.send_message(message.chat.id, help_message)
