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
    update.message