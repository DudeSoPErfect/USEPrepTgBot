import telebot

from paronimy_data_base import data_True, data_False
from user_data import users

import time
import sqlite3 as sql
import random
from telebot import types

TOKEN = "/Your token/"
bot = telebot.TeleBot(TOKEN)
start = 's'  # команда для старта

# !!!

index_image = -1
index_block = -1

# количество вопросов для каждого блока
ranges = [3, 3, 2, 8, 3, 4]


@bot.message_handler(commands=[start])
def register(msg):
    bot.send_message(msg.chat.id, 'введите код доступа')
    bot.register_next_step_handler(msg, text_handler)


def text_handler(msg):
    if msg.text == 'asdf':
        bot.send_message(msg.chat.id, 'Добро пожаловать')
        keyboard = telebot.types.ReplyKeyboardMarkup()
        keyboard.row('Математику', 'Русский язык')

        bot.send_message(msg.chat.id, 'Привет! Что будем тренировать?', reply_markup=keyboard)

        bot.register_next_step_handler(msg, step)
    else:
        bot.send_message(msg.chat.id, 'Пароль неверен')
        bot.register_next_step_handler(msg, register)
        return
def step(msg):
    text = msg.text
    if text == 'Русский язык':
        keyboard = telebot.types.ReplyKeyboardMarkup()
        keyboard.row('Ударения', 'Паронимы')
        bot.send_message(msg.chat.id, 'Отлично! Выберите раздел', reply_markup=keyboard)
        bot.register_next_step_handler(msg, russkiy)
    if text == 'Математику':
        global index_block
        global index_image
        index_block = random.randint(1, 6)
        index_image = random.randint(1, ranges[index_block - 1])
        bot.send_photo(msg.chat.id,
                       photo=open('triga/%d/questions/%d%d.jpg' % (index_block, index_block, index_image), 'rb'))

        bot.send_message(msg.chat.id, '____________')
        for i in range(ranges[index_block - 1]):
            bot.send_photo(msg.chat.id,
                           photo=open('triga/%d/answers/%d%d.jpg' % (index_block, index_block, i + 1), 'rb'))

        mup = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
        b = []
        for i in range(ranges[index_block - 1]):
            b.append(types.KeyboardButton(str(i + 1)))
        for i in b:
            mup.add(i)
        last = types.KeyboardButton('закончить')
        mup.add(last)
        bot.send_message(msg.chat.id, 'Какая картинка соответствует первой?', reply_markup=mup)
        bot.register_next_step_handler(msg, triga)


def russkiy(msg):
    text = msg.text
    if text == 'Ударения':
        markup = telebot.types.ReplyKeyboardRemove(selective=False)


        pool = get_content_from_udarenia()
        exercise = pool[random.randint(0, len(pool) - 1)]

        variants_clav = make_variants_clav(exercise[0])
        bot.send_message(msg.chat.id, exercise[0], reply_markup=variants_clav)
        bot.register_next_step_handler(msg, udarenia)

    if text == 'Паронимы':
        keyboard = telebot.types.ReplyKeyboardMarkup()
        keyboard.row('Теория', 'Практика')
        bot.send_message(msg.chat.id, 'Понял! Изучаем теорию или практикуемся?', reply_markup=keyboard)
        bot.register_next_step_handler(msg, paronimy)


def paronimy(msg):
    text = msg.text
    if text == 'Теория':
        doc = open('Паронимы.docx', 'rb')
        bot.send_document(msg.chat.id, doc)
        bot.send_message(msg.chat.id, 'Высылаю теорию! Удачного изучения!')
    if text == 'Практика':
        markup = telebot.types.ReplyKeyboardRemove(selective=False)
        bot.send_message(msg.chat.id, 'К сожалению, это находиться в стадии разработки:(', reply_markup=markup)
        questions = list(data_True)
        random.shuffle(questions)
        bot.send_message(msg.chat.id, 'Вставьте пропущенное слово')
        global mistakes
        mistakes = []
        global cntr
        for cntr in questions:
            arr = [data_True, data_False]
            random.shuffle(arr)
            x, y = arr[0], arr[1]
            keyboard = telebot.types.ReplyKeyboardMarkup()
            keyboard.row(x[cntr], y[cntr])
            bot.send_message(msg.chat.id, cntr, reply_markup=keyboard)
            bot.register_next_step_handler(msg, cycle)
            global no_answer_yet
            no_answer_yet = True
            while no_answer_yet:
                pass


def cycle(msg):
    global no_answer_yet
    no_answer_yet = False
    text = msg.text
    global cntr
    if text != data_True[cntr]:
        global mistakes
        mistakes.append([cntr, data_True[cntr], data_False[cntr]])
    keyboard = telebot.types.ReplyKeyboardMarkup()
    keyboard.row('Продолжить', 'Завершить')
    bot.register_next_step_handler(msg, next_step)


def next_step(msg):
    text = msg.text
    if text == 'Завершить':
        bot.send_message(msg.chat.id, len(mistakes))


def get_content_from_udarenia():

    with sql.connect("udar.db") as con:
        cur = con.cursor()
        cur.execute("CREATE TABLE IF NOT EXISTS base0("
                    "attempt TEXT,"
                    "answer TEXT,"
                    "right_number INT,"
                    "all_number INT);")
        # считываем с него все данные
        cur.execute("SELECT * FROM base0;")
        data = cur.fetchall()
        con.commit()
    return data



def make_variants_clav(word):
    word = word.lower()
    arr = []
    glasnie = 'уеыаоэяиюё'
    for i in range(len(word)):
        if word[i] in glasnie:
            arr.append(word[:i] + word[i].upper() + word[i + 1:])

    mup = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    b = []
    for i in arr:
        b.append(types.KeyboardButton(i))
    for i in b:
        mup.add(i)
    last = types.KeyboardButton('закончить')
    mup.add(last)
    return mup


def udarenia(msg):
    pool = get_content_from_udarenia()

    if msg.text == 'закончить':
        keyboard = telebot.types.ReplyKeyboardMarkup()
        keyboard.row('Ударения', 'Паронимы')
        bot.send_message(msg.chat.id, 'хорошо', reply_markup=keyboard)
        return

    answer = ''
    for i in pool:
        if msg.text.lower() == i[0]:
            answer = i

    if answer == '':
        exercise = pool[random.randint(0, len(pool) - 1)]

        variants_clav = make_variants_clav(exercise[0])
        bot.send_message(msg.chat.id, 'неверный формат')
        bot.send_message(msg.chat.id, exercise[0], reply_markup=variants_clav)
        bot.register_next_step_handler(msg, udarenia)
        return
    if answer[1] == msg.text:
        bot.send_message(msg.chat.id, 'Вы ответили верно!')
    else:
        bot.send_message(msg.chat.id, 'Вы ответили неверно, верный ответ: %s' % (answer[1]))
    exercise = pool[random.randint(0, len(pool) - 1)]

    variants_clav = make_variants_clav(exercise[0])
    bot.send_message(msg.chat.id, exercise[0], reply_markup=variants_clav)
    bot.register_next_step_handler(msg, udarenia)
    return


def triga(msg):
    answer = 0
    global index_block
    global index_image
    if msg.text == 'закончить':
        keyboard = telebot.types.ReplyKeyboardMarkup()
        keyboard.row('Математику', 'Русский язык')

        msg = bot.send_message(msg.chat.id, 'Что будем тренировать?', reply_markup=keyboard)
        bot.register_next_step_handler(msg, step)
        return
    try:
        answer = int(msg.text)
    except Exception:

        bot.send_message(msg, 'неверный формат')

    if answer == index_image:
        bot.send_message(msg.chat.id, 'верно')

    else:
        bot.send_message(msg.chat.id, 'неверно, верный ответ: %d' % (index_image))

    time.sleep(2)
    index_block = random.randint(1, 6)
    index_image = random.randint(1, ranges[index_block - 1])
    bot.send_photo(msg.chat.id,
                   photo=open('triga/%d/questions/%d%d.jpg' % (index_block, index_block, index_image), 'rb'))

    bot.send_message(msg.chat.id, '____________')
    for i in range(ranges[index_block - 1]):
        bot.send_photo(msg.chat.id,
                       photo=open('triga/%d/answers/%d%d.jpg' % (index_block, index_block, i + 1), 'rb'))

    mup = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    b = []
    for i in range(ranges[index_block - 1]):
        b.append(types.KeyboardButton(str(i + 1)))
    for i in b:
        mup.add(i)
    last = types.KeyboardButton('закончить')
    mup.add(last)
    bot.send_message(msg.chat.id, 'Какая картинка соответствует первой?', reply_markup=mup)
    bot.register_next_step_handler(msg, triga)


bot.polling()
