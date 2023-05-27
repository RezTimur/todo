from telegram.ext import (CommandHandler, ConversationHandler,
                          Filters, MessageHandler, CallbackQueryHandler)

from constants import *
from interrput import *
from telegram.ext import CallbackContext, ConversationHandler
from telegram_bot_calendar import DetailedTelegramCalendar, LSTEP
from telegram import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    Update
)
from datetime import date
from filework import write_csv
from start_menu import get_menu


class MyStyleCalendar(DetailedTelegramCalendar):
    # previous and next buttons style. they are emoji now!
    prev_button = "⬅️"
    next_button = "➡️"
    # you do not want empty cells when month and year are being selected
    empty_month_button = ""
    empty_year_button = ""
    middle_button_year = ""


def add_task(update: Update, context: CallbackContext):
    # update.mesage.reaply_sticker (ADD_STICKER)
    update.message.reply_text(f"Введите текст дела")
    return TASK


def handle_task_text(update: Update, context: CallbackContext):

    message = update.message.text
    context.user_data["todo_text"] = message
    # update.message.reply_text(message)
    calendar, step = MyStyleCalendar(
        locale="ru", min_date=date.today()).build()
    context. bot.send_message(update.effective_chat.id,
                              f"Выберите {RU_STEP[step]}",
                              reply_markup=calendar)
    return DATE


def handel_date(update: Update, context: CallbackContext):
    result, key, step = MyStyleCalendar(
        locale="ru", min_date=date.today()).process(update.callback_query.data)
    if not result and key:
        context.bot.send_message(
            update.effective_chat.id, f"Выберите {RU_STEP[step]}", reply_markup=key)
    elif result:
        delete_message(update, context, end=3)
        year, month, day = str(result).split('-')
        true_date = day + month + "." + year
        context.user_data["date"] = true_date
        context.bot.send_message(
            update.effective_chat.id, f"Вы выбрали {result}")
        mark_up = [[CONTINUE]]
        keyboard = ReplyKeyboardMarkup(
            keyboard=mark_up,
            resize_keyboard=True,
            one_time_keyboard=True
        )
        context.bot.send_message(
            update.effective_chat.id, f'Чтобы продолжить, нажми на "{CONTINUE}"', reply_markup=keyboard)
        return HOUR


def handle_hour(update: Update, context: CallbackContext):
    keyboard = []
    steps = {0: 0, 1: 6, 2: 12, 3: 18}
    for line in range(4):
        keyboard.append([])
        for column in range(6):
            hour = column + steps[line]
            if hour < 10:
                hour = "0" + str(hour)
            keyboard[line].append(InlineKeyboardButton(
                text=f"{hour}:00", callback_data=f"{hour}"))
    murkup = InlineKeyboardMarkup(keyboard)
    context.bot.send_message(
            update.effective_chat.id, f"Выберите час, к коему нужно завершить задачу", reply_markup=murkup)
    return MINUTE


def handle_minute(update: Update, context: CallbackContext):
    hour = update.callback_query.data
    context.user_data["hour"] = hour
    buttons = []
    steps = {0: 0, 1: 3, 2: 6, 3: 9}
    for line in range(4):
        buttons.append([])
        for column in range(3):
            char = ''
            minutes = (column+steps[line]) * 5
            if minutes < 10:
                char = '0'
            buttons[line].append(InlineKeyboardButton(
                f"{hour}:{char}{minutes}", callback_data=f"{char}{minutes}"))

    keyboard = InlineKeyboardMarkup(buttons)
    delete_message(update, context, start=1, end=2)
    context.bot.send_message(
        update.effective_chat.id,
        f"Выбери минуту к которой нужно дело завершить",
        reply_markup=keyboard,
    )
    return RESULT


def save_mesage(update: Update, context: CallbackContext):
    todo_text = context.user_data["todo_text"]
    todo_date = context.user_data["date"]
    hour = context.user_data["hour"]
    minute = update.callback_query.data
    file = context.user_data["file"]
    write_csv(file, [todo_text, todo_date, f"{hour}:{minute}"])
    #   context.bot.send_sticker(update.effective_chat.id,ADD_COMPLETE_STICKER)
    context.bot.send_message(update.effective_chat.id,f"Дело добавлено")
    get_menu(update, context)
    return ConversationHandler.END

        

            

add_handler = ConversationHandler(
    entry_points=[MessageHandler(Filters.regex(f"^{CREATE}$"), add_task)],
    states={
        TASK: [MessageHandler(Filters.text & ~Filters.command, handle_task_text)],
        DATE: [CallbackQueryHandler( handel_date, DetailedTelegramCalendar.func())],
        HOUR: [MessageHandler(Filters.text & ~Filters.command, handle_hour)],
        MINUTE:[CallbackQueryHandler(handle_minute)],
        RESULT:[CallbackQueryHandler(save_mesage)]

    },
    fallbacks=[CommandHandler('finish', endpoint)]
)

