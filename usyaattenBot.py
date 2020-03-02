import telebot
import psycopg2
import psycopg2.extras

TOKEN = '831756841:AAHuLnOXc1POBqHpEOkOjnfxk1n4mS0eNi4'
bot = telebot.TeleBot(TOKEN)

conn = psycopg2.connect (
    host = "localhost",
    database = "Users",
    user = "postgres",
    password = "1235675")
cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)


user_data = {}

class User:
    def __init__(self, first_name):
        self.first_name = first_name
        self.last_name = ''
        self.age = 0


@bot.message_handler(commands=['start', 'help'])
def handle_start(message):
    user_markup = telebot.types.ReplyKeyboardMarkup(True, True) # второе тру - чтобы клава убралась нахуй
    user_markup.row('Создать анкету', 'Искать анкеты')
    bot.send_message(message.from_user.id, 'Че хочешь', reply_markup=user_markup)
    #msg = bot.send_message(message.chat.id, 'Введите имя')
    #bot.register_next_step_handler(msg, process_firstname_step)

@bot.message_handler(content_types=['text'])
def handle_text(message):
    if message.text == 'Создать анкету':
        msg = bot.send_message(message.chat.id, 'Введите имя')
        bot.register_next_step_handler(msg, process_firstname_step)
    elif message.text == 'Искать анкеты':
        bot.send_message(message.from_user.id, 'Введи параметры поиска/ФУНКЦИОНАЛ ЕЩЕ НЕ РЕАЛИЗОВАН')

def process_firstname_step(message):
    try:
        user_id = message.from_user.id
        user_data[user_id] = User(message.text)

        msg = bot.send_message(message.chat.id, "Введите фамилию") #в ПЕРЕМЕННУЮ MSG ЗАПИСЫВАЕТСЯ ФАМИЛИЯ ПОЛЬЗОВАТЕЛЯ
        bot.register_next_step_handler(msg, process_lastname_step)
    except Exception as e:
        bot.reply_to(message, 'Все хуево')

def process_lastname_step(message):
    try:
        user_id = message.from_user.id
        user = user_data[user_id]
        user.last_name = message.text

        sql = "INSERT INTO Persons (user_id, firstname, lastname) VALUES (%s, %s, %s)"
        val = (user_id, user.first_name, user.last_name)
        cur.execute(sql, val)
        conn.commit()

        bot.send_message(message.chat.id, "Вы успешно зарегестрированы")

    except Exception as e:
        bot.reply_to(message, 'Ошибка, или вы уже зарегестрированны')

bot.polling()


