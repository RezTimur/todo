from telegram.ext import CallbackContext
from telegram import (
    Update,
    ReplyKeyboardMarkup
)
from stickers import *
from constants import *
from filework import init


def start(update: Update, context: CallbackContext):
    mark_up = [[GO]]
    keyboard = ReplyKeyboardMarkup(
        keyboard=mark_up,
        resize_keyboard=True,
        one_time_keyboard=True,
        input_field_placeholder=f'Нажми на кнопку "{GO}", поиграем!'
    )
    update.message.reply_sticker(START_STICKER)
    init(update, context)
    update.message.reply_text(
        f'Чтобы начать, нажми на "{GO}"', reply_markup=keyboard)

    return MENU


def get_menu(update: Update, context: CallbackContext):
    name = update.effective_user.full_name
    mark_up = [[CREATE, SHOW, UPDATE], [COMPLETE, DELETE]]
    keyboard = ReplyKeyboardMarkup(
        keyboard=mark_up,
        resize_keyboard=True,
        one_time_keyboard=True
    )
    update.message.reply_sticker(START_STICKER)


    update.message.reply_text(
        f'Выберите, что хотите сделать, мастер {name}?', reply_markup=keyboard)
    return ACTION
