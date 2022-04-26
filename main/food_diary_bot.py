from threading import TIMEOUT_MAX
from matplotlib.pyplot import text
from telebot import types
from src import *
from datetime import datetime as dt
from datetime import timedelta
import pandas as pd
import dataframe_image as dfi
import os
import json
from json import JSONDecodeError


pd.set_option('display.max_colwidth', None)


    
@bot.message_handler(commands=["start"])
def start(message):
    markup = types.ReplyKeyboardMarkup()

    new_meal = types.KeyboardButton('🍽 Добавить прием пищи')
    show_diaries = types.KeyboardButton('📆 Показать даты дневников')
    get_diary = types.KeyboardButton('📒 Получить дневник')


    markup.add(new_meal, get_diary, show_diaries)

    bot.send_message(message.chat.id, 'Привет, {0.first_name}!'.format(message.from_user), reply_markup=markup)




@bot.message_handler(content_types=["text"])
def bot_message(message):

    if message.text == '🍽 Добавить прием пищи':
        markup = types.ReplyKeyboardMarkup()
        breakfast = types.KeyboardButton('🥞 Завтрак')
        lunch = types.KeyboardButton('🍜 Обед')
        dinner = types.KeyboardButton('🥗 Ужин')
        new_snack = types.KeyboardButton('🍏 Перекус')
        back = types.KeyboardButton('🔙 Назад')
        
        markup.add(breakfast, lunch, dinner, new_snack, back)
        bot.send_message(message.chat.id, 'Выберете прием пищи', reply_markup=markup)


    elif message.text == '🔙 Назад':
        # markup = types.ReplyKeyboardMarkup()

        # new_meal = types.KeyboardButton('🍽 Добавить прием пищи')
        # show_diaries = types.KeyboardButton('📆 Показать даты дневников')
        # diary = types.KeyboardButton('📒 Получить дневник')

        # markup.add(new_meal, diary, show_diaries)
        # bot.send_message(message.chat.id, 'Назад', reply_markup=markup)
        msg = bot.send_message(message.chat.id, 'Назад')
        bot.register_next_step_handler(msg, start)
    

    elif message.text == '🥞 Завтрак':
        meal_name = 'Завтрак'

        date_keyboard = types.ReplyKeyboardMarkup()
        key_today = types.KeyboardButton('Сегодня')
        key_yesterday = types.KeyboardButton('Вчера')
        back = types.KeyboardButton('🔙 Назад')
        date_keyboard.add(key_today, key_yesterday, back)

        msg = bot.send_message(message.chat.id, 'Выберете день или введите другую дату', reply_markup=date_keyboard)
        bot.register_next_step_handler(msg, get_date, meal_name)
  

    elif message.text == '🍜 Обед':
        meal_name = 'Обед'

        date_keyboard = types.ReplyKeyboardMarkup()
        key_today = types.KeyboardButton('Сегодня')
        key_yesterday = types.KeyboardButton('Вчера')
        back = types.KeyboardButton('🔙 Назад')
        date_keyboard.add(key_today, key_yesterday, back)

        msg = bot.send_message(message.chat.id, 'Выберете день или введите другую дату', reply_markup=date_keyboard)
        bot.register_next_step_handler(msg, get_date, meal_name)

    elif message.text == '🥗 Ужин':
        meal_name = 'Ужин'

        date_keyboard = types.ReplyKeyboardMarkup()
        key_today = types.KeyboardButton('Сегодня')
        key_yesterday = types.KeyboardButton('Вчера')
        back = types.KeyboardButton('🔙 Назад')
        date_keyboard.add(key_today, key_yesterday, back)

        msg = bot.send_message(message.chat.id, 'Выберете день или введите другую дату', reply_markup=date_keyboard)
        bot.register_next_step_handler(msg, get_date, meal_name)

    elif message.text == '🍏 Перекус':
        meal_name = 'Перекус'

        date_keyboard = types.ReplyKeyboardMarkup()
        key_today = types.KeyboardButton('Сегодня')
        key_yesterday = types.KeyboardButton('Вчера')
        back = types.KeyboardButton('🔙 Назад')
        date_keyboard.add(key_today, key_yesterday, back)

        msg = bot.send_message(message.chat.id, 'Выберете день или введите другую дату', reply_markup=date_keyboard)
        bot.register_next_step_handler(msg, get_date, meal_name)


    elif message.text == '📒 Получить дневник':

        date_keyboard = types.ReplyKeyboardMarkup()
        key_today = types.KeyboardButton('Сегодня')
        key_yesterday = types.KeyboardButton('Вчера')
        back = types.KeyboardButton('🔙 Назад')
        date_keyboard.add(key_today, key_yesterday, back)

        bot_text =  'За какой день нужен дневник?\nВыберете день или введите другую дату в формате DD.MM.YY'
        msg = bot.send_message(message.chat.id, bot_text, reply_markup=date_keyboard)
        bot.register_next_step_handler(msg, get_diary)


    elif message.text == '📆 Показать даты дневников':
        try:
            file = open(os.getcwd() + '/data/diaries.json', 'r')
            diary = json.load(file)
            file.close()
            
            diaries_dates = ', '.join(list(diary.keys()))
            msg =  bot.send_message(message.chat.id, 'Даты дневников: {}'.format(diaries_dates))
            bot.register_next_step_handler(msg, start)

        except JSONDecodeError:
            msg =  bot.send_message(message.chat.id, 'В дневнике нет записей')
            bot.register_next_step_handler(msg, start)


def get_date(message, meal_name):
    try:
        if message.text == 'Сегодня':
            date = dt.now().strftime("%d.%m.%y")
        elif message.text == 'Вчера':
            date = (dt.now() - timedelta(days=1)).strftime("%d.%m.%y")
        else:
            dt.strptime(message.text, '%d.%m.%y') 
            date = message.text

        msg = bot.send_message(message.chat.id, 'Укажите время в формате HH:MM')
        bot.register_next_step_handler(msg, get_time, meal_name, date) 
    except ValueError:
        bot.send_message(message.from_user.id, "Неверный формат даты. Проверьте корректность введенных данных")
        bot.register_next_step_handler(message, get_date, meal_name)

    

def get_time(message, meal_name, date): 
    if meal_name != 'Перекус':
        try:
            dt.strptime(message.text, "%H:%M") 
            
            meal = make_meal(meal_name)
            meal[meal_name]['Время'] = message.text
            msg = bot.send_message(message.chat.id, 'Укажите уровень голода')
            bot.register_next_step_handler(msg, get_hunger, meal_name, meal, date)

        except ValueError:
            msg = bot.send_message(message.chat.id, 'Неверный формат времени. Проверьте корректность введенных данных')
            bot.register_next_step_handler(msg, get_time, meal_name, date) 
    else:
        try:
            dt.strptime(message.text, "%H:%M") 
            
            meal = make_meal(meal_name)
            meal[meal_name]['Время'] = message.text
            msg = bot.send_message(message.chat.id, 'Укажите продукты')
            bot.register_next_step_handler(msg, get_composition_snak, meal_name, meal, date)

        except ValueError:
            msg = bot.send_message(message.chat.id, 'Неверный формат времени. Проверьте корректность введенных данных')
            bot.register_next_step_handler(msg, get_time, meal_name, date) 


def get_hunger(message, meal_name, meal, date):
    meal[meal_name]['Уровень голода'] = message.text
    msg = bot.send_message(message.chat.id, 'Укажите уровень насыщения')
    bot.register_next_step_handler(msg, get_saturation, meal_name, meal, date) 


def get_saturation(message, meal_name, meal, date):
    meal[meal_name]['Уровень насыщения'] = message.text
    msg = bot.send_message(message.chat.id, 'Укажите продукты')
    bot.register_next_step_handler(msg, get_composition, meal_name, meal, date) 


def get_composition(message, meal_name, meal, date):
    meal[meal_name]['Состав'] = message.text

    try:
        write_file = open(os.getcwd() + '/data/diaries.json', 'r')
        diary = json.load(write_file)
        write_file.close()

        add_record(diary, date, meal)

        write_file = open(os.getcwd() + '/data/diaries.json', 'w')
        json.dump(diary, write_file, indent=4)
        write_file.close()
    except JSONDecodeError:
        diary = {}
        add_record(diary, date, meal)

        write_file = open(os.getcwd() + '/data/diaries.json', 'w')
        json.dump(diary, write_file, indent=4)
        write_file.close()

    msg = bot.send_message(message.chat.id, 'Прием пищи добавлен')
    start(msg)


def get_composition_snak(message, meal_name, meal, date):
    meal[meal_name]['Состав'] = message.text

    try:
        write_file = open(os.getcwd() + '/data/diaries.json', 'r')
        diary = json.load(write_file)
        write_file.close()

        add_record_snak(diary, date, meal, meal_name)

        write_file = open(os.getcwd() + '/data/diaries.json', 'w')
        json.dump(diary, write_file, indent=4)
        write_file.close()
    except JSONDecodeError:
        diary = {}
        add_record_snak(diary, date, meal, meal_name)
        write_file = open(os.getcwd() + '/data/diaries.json', 'w')
        json.dump(diary, write_file, indent=4)
        write_file.close()

    msg = bot.send_message(message.chat.id, 'Перекус добавлен добавлен')
    start(msg)


def get_diary(message):
    if message.text == '🔙 Назад':
        start(message)
    else:
        try:
            if message.text == 'Сегодня':
                diary_date = dt.now().strftime("%d.%m.%y")
            elif message.text == 'Вчера':
                diary_date = (dt.now() - timedelta(days=1)).strftime("%d.%m.%y")
            else:
                dt.strptime(message.text, '%d.%m.%y') 
                diary_date = message.text

            #read 
            file = open(os.getcwd() + '/data/diaries.json', 'r')
            diary = json.load(file)
            file.close()

            if diary_date  not in list(diary.keys()):
                msg = bot.send_message(message.chat.id, 'Дневника с такой датой нет. Введите другую дату')
                bot.register_next_step_handler(msg, get_diary)
            else:
                diary_for_day = diary.get(diary_date)

                df = pd.DataFrame(diary_for_day).T
                png_path = os.getcwd() + '/data/img/mytable.png'

                dfi.export(df, png_path)

                table_png = open(png_path, 'rb')
                bot.send_photo(message.chat.id, table_png)
                msg = bot.send_message(message.chat.id, 'Дневник за {}'.format(diary_date))
                bot.register_next_step_handler(msg, start)
        
        except ValueError:
            bot.send_message(message.from_user.id, "Неверный формат даты. Проверьте корректность введенных данных")
            bot.register_next_step_handler(message, get_diary)




# Запускаем бота
bot.polling(none_stop=True, interval=0)







