import telebot
from telebot import types
import psycopg2
import psycopg2.extras

TOKEN = '831756841:AAHuLnOXc1POBqHpEOkOjnfxk1n4mS0eNi4'
bot = telebot.TeleBot(TOKEN)

conn = psycopg2.connect (
    host = "localhost",
    database = "postgres",
    user = "postgres",
    password = "1235675")
cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

name1 = ''
surname1 = ''
age1 = 0
tg_id1 = 0
result = 0
an = ''
b = 0


@bot.message_handler(content_types=['text'])

def start(message):
    global tg_id1
    global result
    global an
    tg_id1 = message.chat.id

    if message.text == '/reg':
        sql = "SELECT EXISTS (SELECT * FROM users_tg_bot WHERE tg_id = %s)" #SELECT EXISTS (
        var = (tg_id1,)
        cur.execute(sql, var)
        result = cur.fetchall()
        print(result)

        if result[0][0] == 0:
            bot.send_message(message.from_user.id, "Как тебя зовут?")
            bot.register_next_step_handler(message, get_name)
        else:
            bot.send_message(message.from_user.id, "Вы уже зарегестрированы!")

    elif message.text == "/show":
        cur.execute('''SELECT * FROM users_tg_bot
                    ORDER BY RANDOM()
                    LIMIT 1''')
        an = cur.fetchall()
        bot.send_message(message.from_user.id, text = an)
        print(*an)

    else:
        bot.send_message(message.from_user.id, 'Напиши /reg')

def get_name(message):
    global name1
    name1 = message.text
    bot.send_message(message.from_user.id, "Какая у тебя фамилия?")
    bot.register_next_step_handler(message, get_surname)

def get_surname(message):
    global surname1
    surname1 = message.text
    bot.send_message(message.from_user.id, "Сколько тебе лет?")
    bot.register_next_step_handler(message, get_age)

def insert_to_db(name, surname, age):
    sql = ("INSERT INTO USERS_TG_BOT (NAME, SURNAME, AGE, TG_ID) VALUES (%s, %s, %s, %s)")
    val = (name, surname, age, tg_id1)
    cur.execute(sql, val)
    conn.commit()

def get_age(message):
    global age1
    while age1 == 0:
        try:
            age1 = int(message.text)
        except Exception:
            bot.send_message(message.from_user.id, "Напиши возраст корректно, мудила")
    keyboard = types.InlineKeyboardMarkup() #клавиатура????
    key_yes = types.InlineKeyboardButton(text='Да', callback_data='yes')  # кнопка «Да»
    keyboard.add(key_yes)  # добавляем кнопку в клавиатуру
    key_no = types.InlineKeyboardButton(text='Нет', callback_data='no')
    keyboard.add(key_no)
    question = 'Тебе ' + str(age1) + ' лет, тебя зовут ' + name1 + ' ' + surname1 + '?'
    bot.send_message(message.from_user.id, text = question, reply_markup=keyboard)

    insert_to_db(name1, surname1, age1)


@bot.callback_query_handler(func=lambda call: True)
def callback_worker(call):
    if call.data == "yes":
        bot.send_message(call.message.chat.id, 'Запомню : )')
    elif call.data == "no":
        bot.send_message(call.message.chat.id, "Пошел нахуй, наебщик")

bot.polling()

