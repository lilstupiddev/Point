import telebot
import config
from telebot import types
from database import Database

db = Database('bot/db.db') 
bot = telebot.TeleBot(config.TOKEN)

@bot.message_handler(commands = ['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard = True)
    item1 = types.KeyboardButton('Пошук співрозмовника')
    markup.add(item1)
    bot.send_message(message.chat.id, "Привіт, {0.first_name}! Вітаємо вас в анонімному чаті, де ви зможете поділитися з іншою людиною своїми емоціями, підтримати один одного! Натискайте на пошук співрозмовника!".format(message.from_user), reply_markup = markup)



@bot.message_handler(commands = ['menu'])
def menu(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard = True)
    item1 = types.KeyboardButton('Пошук співрозмовника')
    markup.add(item1)
    bot.send_message(message.chat.id, "Меню".format(message.from_user), reply_markup = markup)


@bot.message_handler(commands = ['stop'])
def stop(message):
    chat_info = db.get_active_chat(message.chat.id)
    if chat_info != False:
        db.delete_chat(chat_info[0])
        markup = types.ReplyKeyboardMarkup(resize_keyboard = True)
        item1 = types.KeyboardButton('Пошук співрозмовника')
        markup.add(item1)

        bot.send_message(chat_info[1], 'Співрозмовник вийщов з чату', reply_markup = markup)
        bot.send_message(message.chat.id, 'Ви вийшли з чату', reply_markup = markup)
    else:
        bot.send_message(message.chat.id, 'Ви не почали розмову', reply_markup = markup)

@bot.message_handler(content_types=['text'])
def bot_message(message):
    if message.chat.type == 'private':
        if message.text == 'Пошук співрозмовника':
                markup = types.ReplyKeyboardMarkup(resize_keyboard = True)
                item1 = types.KeyboardButton('Закінчити пошук')
                markup.add(item1)
                
                chat_two = db.get_chat()

                if db.create_chat(message.chat.id, chat_two) == False:
                    db.add_queue(message.chat.id)
                    bot.send_message(message.chat.id, 'Пошук співрозмовника', reply_markup =  markup)
                else:
                    mess = 'Співрозмовника знайдено! Якщо ви хочете зупинити розмову, то вам потрібно натиснути /stop'
                    markup = types.ReplyKeyboardMarkup(resize_keyboard = True)
                    item1 = types.KeyboardButton('/stop')
                    markup.add(item1)

                    bot.send_message(message.chat.id, mess, reply_markup = markup)
                    bot.send_message(chat_two, mess, reply_markup = markup)

        elif message.text == 'Закінчити пошук':
            db.delete_queue(message.chat.id)
            bot.send_message(message.chat.id, 'Пошук зупинено, напишіть /menu')

        else:
            chat_info = db.get_active_chat(message.chat.id)
            bot.send_message(chat_info[1], message.text)

bot.polling(none_stop = True)