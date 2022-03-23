import os
import telebot
import logging
import psycopg2
from flask import Flask, request
from ilitaconfig import token_telegram, app_url, db_uri

bot = telebot.TeleBot(token_telegram)
server = Flask(__name__)
logger = telebot.logger
logger.setLevel(logging.DEBUG)

db_connection = psycopg2.connect(db_uri, sslmode='require')
db_object = db_connection.cursor()

def update_messages_count(user_id):  #я не понимаю, почему db_object не работает, если его вынести в друой файл
    db_object.execute(f'UPDATE slawe SET messages = messages + 1 WHERE id = {user_id}')
    db_connection.commit()

@bot.message_handler(commands=['start'])
def start(message):
    id_user = message.from_user.id
    bot.reply_to(message, 'Hello, ' + message.from_user.first_name)
    update_messages_count(id_user)


@bot.message_handler(commands=['help'])
def help_bot(message):
    id_user = message.from_user.id
    bot.reply_to(message, 'Сейчас бот отлавливает все соси и извинения, вскоре добавим и борьбу')
    update_messages_count(id_user)

@bot.message_handler(commands=['create_slave'])
def create_slave(message):
    if len(message.text) > len('/create_slave '):
        name_slave = message.text[len('/create_slave '):]
        user_id = message.from_user.id
        db_object.execute(f'SELECT id FROM slawe WHERE id = {user_id}')
        result = db_object.fetchone()
        if not result:
            bot.reply_to(message, 'Чичас придумаем тебе слейва')
            print('cоздаем пользователя ' + name_slave)
            db_object.execute("INSERT INTO slawe(id, slave_name, messages, day_activ, weight, win_stats, loss_stats) VALUES(%s, %s, %s, %s, %s, %s, %s)",
                              (user_id, name_slave, 0, 0, 30, 0, 0))
            db_connection.commit()
            bot.reply_to(message, '/Проверь сейчас /stats')
        else:
            bot.reply_to(message, 'У тебя уже есть слейв, но функцию смены имени еще не написали')
    else:
        bot.reply_to(message, 'Ты не написал имя после команды')
    update_messages_count(user_id)


@bot.message_handler(commands=['stats'])
def get_stats_spamerow(message):
    db_object.execute("SELECT * FROM slawe ORDER BY messages DESC LIMIT 10")
    result = db_object.fetchall()

    if not result:
        bot.reply_to(message, 'Нет данных...')
    else:
        reply_message = '- Топ флудеров:\n'
        for i, item in enumerate(result):
            reply_message += f'{i + 1}. {item[1].strip()} : {item[2]} messages.\n'
        bot.reply_to(message, reply_message)

    update_messages_count(message.from_user.id)


@bot.message_handler(func=lambda m: True)
def gachi_requests(message):
    if message.text.lower() == 'бип':
        print("буп прошел успешно")
        bot.send_message(message.chat.id, "буп")
    elif 'соси' in message.text.lower() or 'sosi' in message.text.lower() or \
            'саси' in message.text.lower() or 'sasi' in message.text.lower():
        bot.reply_to(message, f'Сам соси, {message.from_user.first_name}')
        # Только для беседы, в личке не from_user, a chat
    elif 'извини' in message.text.lower() or 'sorry' in message.text.lower() \
            or 'прости' in message.text.lower() or 'прошу прощения' in message.text.lower():
        bot.reply_to(message, f'Sorry for what, {message.from_user.first_name}?')
    else:
        pass
    update_messages_count(message.from_user.id)

@server.route('/' + token_telegram, methods=['POST'])
def get_message():  #для переправочки данных в тгбота
    json_string = request.get_data().decode('utf-8')
    update = telebot.types.Update.de_json(json_string)
    bot.process_new_updates([update])
    return '!', 200


@server.route('/')
def webhook():  #высылает ошибки на хероку
    bot.remove_webhook()
    bot.set_webhook(url=app_url)
    return '!', 200


if __name__ == '__main__':
    server.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
