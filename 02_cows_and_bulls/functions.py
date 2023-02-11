from telegram.ext import CallbackContext, ConversationHandler
from telegram import Update,ReplyKeyboardMarkup,ReplyKeyboardRemove
import random

GO = "let's go"
BEGIN,LEVEL,GAME = 1,2,3
EASY,MEDIUM,HARD ="Простой","Средний","Средний"

def start(update:Update, context: CallbackContext):
    mark_up = [[GO]]
    Keyboard = ReplyKeyboardMarkup(
        keyboard=mark_up,
        resize_keyboard=True,
        one_time_keyboard = True,
        input_field_placeholder = f'Нажми на кнопку "{GO}",поиграем '     


    )
    # update.message.reply_text()
    update.message.reply_text(
        f'Чтобы начать, нажми на "{GO}', reply_markup=Keyboard    )
    return BEGIN

def begin(update:Update,context: CallbackContext):
    # если ключа "секретное число" нет в рюкзаке
    secret_number = random.randint(1000, 9999)
    context.user_data['секретное число'] = secret_number
    update.message.reply_text('Напиши число')
    input_field_placeholder=f'
    # создается "секретное число" в рюкзаке
    return  GAME


def game(update: Update, context: CallbackContext):  # callback'
    message = update.message.text
    secret_number = context.user_data['секретное число']  # достаем из рюкзака
    if len(message) != 4 and not message.isdigit():#не число
        update.message.reply_text("Вводить можно только четырехзначные числа!")
        return#выход из функции
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