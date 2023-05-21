from config import TOKEN
from telegram.ext import (
    Updater,
    Filters,
    MessageHandler,
    CommandHandler,
    ConversationHandler
)
from start_menu import *
from interrput import *
from task_create import add_handler


updater = Updater(TOKEN)
dispatcher = updater.dispatcher

conv_handler = ConversationHandler(
    entry_points=[CommandHandler('start', start)], # точка входа
    states={ #шаги
        MENU: [MessageHandler(Filters.text, get_menu)],
        ACTION:[
            add_handler,
            MessageHandler(Filters.text & ~Filters.command, wrong_message)        
        ]
    },
    fallbacks=[CommandHandler('end', end)] # точка выхода
)


dispatcher.add_handler(conv_handler)

print('Сервер запущен!')
updater.start_polling()
updater.idle()  # ctrl + C