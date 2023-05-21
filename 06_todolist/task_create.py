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
        year,month,day = str(result).split('-')
        true_date = day+ month +"."+ year
        context.bot.send_message(
            update.effective_chat.id, f"Вы выбрали {result}")
        
def handle_hour(update: Update, context: CallbackContext):
    keybord = []
    steps = {1: 0, 2: 6, 3: 12, 4: 18}
    for line in range(4):
        keyboard.append([])
        for column in range(6):
            keyboard[line].append(InlineKeyboardButton(text=f"{column} + {steps[line-1]}"))

    murkup = InlineKeyboardMarkup(keyboard)
    context.bot.send_message(
            update.effective_chat.id, f"Выберите час, к коему нужно завершить задачу")


add_handler = ConversationHandler(
    entry_points=[MessageHandler(Filters.regex(f"^{CREATE}$"), add_task)],
    states={
        TASK: [MessageHandler(Filters.text & ~Filters.command, handle_task_text)],
        DATE: [CallbackQueryHandler(
            handel_date, DetailedTelegramCalendar.func())]
    },
    fallbacks=[CommandHandler('finish', endpoint)]
)

