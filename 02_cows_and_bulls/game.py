from config import TOKEN
from telegram.ext import Updater, Filters, MessageHandler,CommandHandler,ConversationHandler
from functions import *

GO = "Вперед"


dialog_handler = ConversationHandler(
    entry_points=[CommandHandler('start', start)],
    states={
        BEGIN: [MessageHandler(Filters.text & ~Filters.command, begin)],

        GAME: [MessageHandler(Filters.text & ~Filters.command, game)]
    },
    fallbacks=[CommandHandler('end',end)]
    
)



updater = Updater(TOKEN)
dispatcher = updater.dispatcher



dispatcher.add_handler(dialog_handler)

print('Сервер запущен')
updater.start_polling()
updater.idle()




game_handler = CommandHandler(Filters.text, game)
dispatcher.add_handler(game_handler)

print('Приложение запущено')
updater.start_polling()
updater.idle()  # ctrl + C
