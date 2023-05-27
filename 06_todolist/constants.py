from telegram import ReplyKeyboardMarkup

GO = 'Поехали'
CONTINUE = 'Продолжить'
MENU, ACTION, TASK, DATE, HOUR, MINUTE, RESULT = range(7)

CREATE = "Создать"
SHOW = "Показать все дела"
UPDATE = "Изменить"
COMPLETE ="Дело сделано"
DELETE = "Удалить дело"


RU_STEP = {'y':'год','m':'месяц', 'd': 'день'}

mark_up = [[CREATE, SHOW, UPDATE], [COMPLETE, DELETE]]
keyboard = ReplyKeyboardMarkup(
    keyboard=mark_up,
    resize_keyboard=True,
    one_time_keyboard=True
)
