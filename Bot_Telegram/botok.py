import telebot
import config

bot = telebot.TeleBot(config.TOKEN)

#@bot.message_handler(content_types = ['text'])
#def func (messgae):
#    bot.send_message(messgae.chat.id, messgae.text)


@bot.message_handler(commands = ['start'])
def welcome_wrapper (message):
    bot.register_next_step_handler(message, welcome)

def welcome(msg):
    bot.reply_to(msg, "Иди нахуй со своим " + msg.text)
    bot.register_next_step_handler(msg, welcome1)

def welcome1(msg):
    bot.reply_to(msg, "Да о5 иди нахуй с " + msg.text)


@bot.message_handler(commands = ['reverse'])
def reverse_wrapper(msg):
    bot.reply_to(msg, msg.text[::-1])

bot.infinity_polling()