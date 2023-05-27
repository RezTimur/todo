import csv
import os
from telegram.ext import CallbackContext
from telegram import (
    Update
)
from stickers import *
from constants import *



def read_csv(filename):
    with open(filename, 'r', encoding='utf-8') as file:
        quest = list(csv.reader(file, delimiter='|'))
        return quest

def write_csv(filename,line_to_line):  
    with open(filename, 'a', encoding='utf-8') as file:
        worker = csv.writer(file, delimiter='|',lineterminator='\n')  # \n - это перенос
        worker.writerow(line_to_line)

def read_todos(update:Update)        


def init(update: Update, context: CallbackContext):
    username = update.effective_user.username
    filename = f'database/{username}.csv'
    context.user_data['file'] = filename
    if not os.path.exists('database'):
        os.mkdir('database')
    if not os.path.exists(filename):
        open(filename,  'w')
