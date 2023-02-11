from telegram.ext import CallbackContext, ConversationHandler
from telegram import Update, ReplyKeyboardMarkup, ReplyKeyboardRemove
import pymorphy2

morph = pymorphy2.MorphAnalyzer()
GO = "Вперед" # то, что написано на кнопке
BEGIN,GAME = 1,2# 1 шаг разговора

def start(update: Update, context: CallbackContext):
    button = [[GO]]
    keyboard = ReplyKeyboardMarkup(button, resize_keyboard=True,
                                   one_time_keyboard=True,
                                   input_field_placeholder='Нажми на кнопку')
    update.message.reply_text(
        f"""Ты любишь придумывать сказки? 
        Я очень люблю. Ты знаешь сказку как посадил дед репку?
        А кто помогал деду репку тянуть? Чтобы начать, нажми на кнопку {GO}!""" , 
        reply_markup=keyboard)
    return BEGIN # переход к следующему шагу

def begin(update: Update, context: CallbackContext):
    heroes = [['дедку'], ['дедка', "репку"]] 
    context.user_data['heroes'] = heroes 
    update.message.reply_text('''
                              Посадил дед репку. Выросла репка большая-пребольшая.
                              Стал дед репку из земли тянуть. Тянет-потянет - вытянуть не может.
                              Кого позвал дедка?
                               ''',  reply_markup=ReplyKeyboardRemove() )

    return GAME

def game(update: Update, context: CallbackContext):
    text = update.message.text
    text = morph.parse(text)[0] # тег - все характеристики слова
    if   text.tag.animacy == "anim": 
        nomn = text.inflect({'nomn'}).word
        accs = text.inflect({'nomn'}).word
        heroes = context.user_data["heroes"]
        update.message.reply_text(f'{nomn}, {accs}')
        heroes[0].insert(0, nomn)
        heroes.insert(0, [accs])
        answer = f"Я {nomn}. Буду помогать. "
        for nom,acc in heroes[1:]:
            answer += f'{nom} за {acc}. '
        answer += "Тянут-потянут - вытянуть не могут."
        update.message.reply_text(f'{answer}')
    else:
        update.message.reply_text(f'Долго  искали мы {text.normal_form} : ничего не нашли')

def end(update: Update, context: CallbackContext):
    update.message.reply_text('Значит, ты выбрал конец')
    return ConversationHandler

