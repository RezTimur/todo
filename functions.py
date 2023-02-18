from telegram.ext import CallbackContext, ConversationHandler
from telegram import Update, ReplyKeyboardMarkup, ReplyKeyboardRemove
import random

GO = "Вперед"
BEGIN, LEVEL, GAME = range(3)
EASY, MEDIUM, HARD = "Простой", "Средний", "Сложный"


def start(update: Update, context: CallbackContext):
    mark_up = [[GO]]
    Keyboard = ReplyKeyboardMarkup(
        keyboard=mark_up,
        resize_keyboard=True,
        one_time_keyboard=True,
        input_field_placeholder=f'Нажми на кнопку "{GO}",поиграем '


    )
    # update.message.reply_text()
    update.message.reply_text(
        f'Чтобы начать, нажми на "{GO}', reply_markup=Keyboard)
    return BEGIN


def begin(update: Update, context: CallbackContext):
    mark_up = [[EASY, MEDIUM, HARD]]
    Keyboard = ReplyKeyboardMarkup(
        keyboard=mark_up,
        resize_keyboard=True,
        one_time_keyboard=True,
        input_field_placeholder=f'{EASY} - 3 буквы'


    )
    # update.message.reply_text()
    update.message.reply_text(
        f'Выбери уровень сложности или нажми /end, чтобы не играть', reply_markup=Keyboard)
    return LEVEL


def level(update: Update, context: CallbackContext):
    level_storage = update.message.text
    if level_storage == EASY:
        with open("02_cows_and_bulls\easy.txt", encoding="utf-8") as file:
            words = file.read().split("\n")
    elif level_storage == MEDIUM:
        with open("02_cows_and_bulls\medium.txt", encoding="utf-8") as file:
            words = file.read().split("\n")
    elif level_storage == HARD:
        with open("02_cows_and_bulls\hard.txt", encoding="utf-8") as file:
            words = file.read().split("\n")
    else:
        update.message.reply_text("Недоступен Файл")
    word = random.choice(words)
    context.user_data["word"] = word
    update.message.reply_text(f'Было выбрано слово {word}')
    return GAME
        
    


def game(update: Update, context: CallbackContext):  # callback'
    message = update.message.text
    secret_number = context.user_data['секретное число']  # достаем из рюкзака
    if len(message) != 4 and not message.isdigit():  # не число
        update.message.reply_text("Вводить можно только четырехзначные числа!")
        return  # выход из функции
    cows = 0
    bulls = 0
    secret_number = str(secret_number)
    for mesto, chislo in enumerate(message):
        if chislo in secret_number:
            if message[mesto] == secret_number[mesto]:
                bulls += 1
            else:
                cows += 1
    update.message.reply_text(f'В вашем числе {cows} коров и {bulls} быков')
    if bulls == 4:
        update.message.reply_text('Вы угадали! Вы красавчик')
        del context.user_data['секретное число']


def end(update: Update, context: CallbackContext):
    update.message.reply_text('Значит, ты выбрал конец')
    return ConversationHandler.END
