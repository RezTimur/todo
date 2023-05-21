import csv
from telegram.ext import CallbackContext, ConversationHandler
from telegram import (
    Update,
    ReplyKeyboardMarkup,
    ReplyKeyboardRemove
)
import random

GO = 'Поехали'
GAME = 1
QUSTIONS_ON_ROND = 7


def start(update: Update, context: CallbackContext):
    mark_up = [[GO]]
    keyboard = ReplyKeyboardMarkup(
        keyboard=mark_up,
        resize_keyboard=True,
        one_time_keyboard=True,
        input_field_placeholder=f'Нажми на кнопку "{GO}", поиграем!'
    )
    # update.message.reply_sticker(START_STICKER)
    update.message.reply_text(
        'Добро пожаловать в викторину! Выбирайте правильный ответ')
    update.message.reply_text(
        f'Чтобы начать, нажми на "{GO}"', reply_markup=keyboard)
    questions = read_csv() # берем все вопросы
    random.shuffle(questions)
    questions = questions[QUSTIONS_ON_ROND:]
    context.user_data["вопросы"] = questions
    context.user_data["right_answer"] = GO
    context.user_data["вопросы"] = questions
    context.user_data["сч"]
    return GAME


def game(update: Update, context: CallbackContext):
    questions = context.user_data["вопросы"]
    #взять ответ пользователя
    #взять из рюкзака правильный ответ

    answers = questions.pop()
    questions_text = answers.pop(0)
    right_answer = answers[0]
    #сохранить правильный ответ в рюкзак
    random.shuffle(answers)
    mark_up = [answers[:2],answers[2:]]
    keyboard = ReplyKeyboardMarkup(
        keyboard=mark_up,
        resize_keyboard=True
    )
    update.message.reply_text(questions_text, reply_markup=keyboard)
    
    #подумай, где должна быть эта часть
    user_answer = update.message.edit_text
    if user_answer == right_answer:
        update.message.reply_sticker('CAACAgIAAxkBAAIW82QV5rWduljXPVx06I4PYyfOE9wpAAIJAQACihKqDtIgSfPqZhBdLwQ')
    elif user_answer == GO:
        pass
    else:
        update.message.reply_sticker('CAACAgIAAxkBAAIW9mQV5r0cGE-o2fa59iRz6iLuGHclAAIgAQACihKqDo73SNr_IzmSLwQ')


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