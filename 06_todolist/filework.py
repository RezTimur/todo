import csv
import os
import csv
from telegram.ext import CallbackContext
from telegram import (
    Update
)
from stickers import *
from constants import *



def read_csv():
    with open('05_quiz\вопросы.csv', 'r', encoding='utf-8') as file:
        quest = list(csv.reader(file, delimiter='|'))
        return quest

    


def write_csv():
    with open('05_quiz\вопросы.csv', 'a', encoding='utf-8') as file:
        worker = csv.writer(file, delimiter='|',lineterminator='\n')  # \n - это перенос
        worker.writerow(['Какая столица Татарстана?',
                        'Казань', 'Астана', 'Елабуга', 'Челны'])
        

def init(update: Update, context: CallbackContext):
    username = update.effective_user.username
    filename = f'database/{username}.csv'
    context.user_data['file'] = filename
    if not os.path.exists('database'):
        os.mkdir('database')
    if not os.path.exists(filename):
        open(filename,  'w')
