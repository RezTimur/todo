from telegram.ext import CallbackContext, ConversationHandler
from telegram import (
    Update
)
from stickers import *
from constants import *


def end(update: Update, context: CallbackContext):  # точка выхода
    name = context.user_data['имя']
    update.message.reply_text(f"Значит, ты выбрал конец, {name}. Если хотите начать заново, нажмите /start")
    return ConversationHandler.END

def wrong_message(update:Update, context: CallbackContext):
    update.message.reply_sticker(
        'CAACAgUAAxkBAAIOx2N4mLSkQWGFUqqzpaTTmfmqizeeAAKBCAACxlHGFZXfauYX-8AwKwQ')
    update.message.reply_text('Такой команды нет', reply_markup=keyboard)

def endpoint(update: Update, context: CallbackContext):
    update.message.reply_text('Вы решили не добавлять дело')
    return ConversationHandler.END

def delete_message(update: Update, context: CallbackContext, start=0, end=1):
    try:
        for i in range(start,end):
            context.bot.delete_message(update.effective_chat.id,update.effective_message.message_id - i)
    except:
        pass

