import csv
from telegram.ext import CallbackContext, ConversationHandler
from telegram import (
    Update,
    ReplyKeyboardMarkup,
    ReplyKeyboardRemove
)
import random
from stickers import *
from constants import *

GO = 'Поехали'




def start(update: Update, context: CallbackContext):
    mark_up = [[GO]]
    keyboard = ReplyKeyboardMarkup(
        keyboard=mark_up,
        resize_keyboard=True,
        one_time_keyboard=True,
        input_field_placeholder=f'Нажми на кнопку "{GO}", поиграем!'
    )
    update.message.reply_sticker(START_STICKER)
    update.message.reply_text(
        '')
    update.message.reply_text(
        f'Чтобы начать, нажми на "{GO}"', reply_markup=keyboard)
    
    return 

def get_menu(update: Update, context: CallbackContext):
    mark_up = [[CREATE, SHOW, UPDATE ], [COMPLETE,DELETE ] ]
    keyboard = ReplyKeyboardMarkup(
        keyboard=mark_up,
        resize_keyboard=True,
        one_time_keyboard=True
    )
    update.message.reply_sticker(START_STICKER)
    update.message.reply_text(
        '')


def end(update: Update, context: CallbackContext):  # точка выхода
    name = context.user_data['имя']
    update.message.reply_text(f"Значит, ты выбрал конец, {name}. Если хотите начать заново, нажмите /start")
    return ConversationHandler.END


def read_csv():
    with open('05_quiz\вопросы.csv', 'r', encoding='utf-8') as file:
        quest = list(csv.reader(file, delimiter='|'))
        return quest

    


def write_csv():
    with open('05_quiz\вопросы.csv', 'a', encoding='utf-8') as file:
        worker = csv.writer(file, delimiter='|',lineterminator='\n')  # \n - это перенос
        worker.writerow(['Какая столица Татарстана?',
                        'Казань', 'Астана', 'Елабуга', 'Челны'])