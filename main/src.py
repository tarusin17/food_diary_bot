from collections import UserString
from datetime import datetime as dt
import telebot
import json
import os


token_file = open(os.getcwd() + '/main/tokens.json', 'r')
token = json.load(token_file)
token_file.close()

TOKEN = token.get("food_diary_token")
bot = telebot.TeleBot(TOKEN)


def make_meal(name, hunger='', saturation='', comp='', time=dt.now().strftime("%H:%M")):
    """Create new meal"""
    return {
        name:{
            'Время':time,
            'Состав':comp,
            'Уровень голода':hunger,
            'Уровень насыщения':saturation
        }
    }


def add_record(directory, date, record):
    directory.setdefault(date, {})
    directory[date].update(record)


def add_record_snak(directory, date, record, meal_name):
    directory.setdefault(date, {})
    
    if directory[date].get(meal_name) == None:
        directory[date].update(record)
    else:
        time = record.get(meal_name).get('Время')
        directory[date][meal_name]['Время'] = directory[date][meal_name]['Время'] + ', ' + time
        
        comp = record.get(meal_name).get('Состав')
        directory[date][meal_name]['Состав'] = directory[date][meal_name]['Состав'] + ', ' + comp





















