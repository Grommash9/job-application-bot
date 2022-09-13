from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup

from bot_app.models.params import Params, Param


def start_application():
    m = InlineKeyboardMarkup()
    m.add(InlineKeyboardButton('Пройти тест', callback_data='start-application'))
    return m


def money_markup():
    m = InlineKeyboardMarkup()
    m.add(InlineKeyboardButton('✔️Да', callback_data='money-yes'))
    m.insert(InlineKeyboardButton('❌Нет', callback_data='money-no'))
    return m


def relocate_markup():
    m = InlineKeyboardMarkup()
    m.add(InlineKeyboardButton('✔️Да', callback_data='relocate-yes'))
    m.insert(InlineKeyboardButton('❌Нет', callback_data='relocate-no'))
    m.add(InlineKeyboardButton('👩Хочу жить с мамой', callback_data='relocate-mom'))
    return m


def age_markup():
    m = InlineKeyboardMarkup(row_width=5)
    for ages in range(18, 24):
        m.insert(InlineKeyboardButton(str(ages), callback_data=f'age-{ages}'))
    return m


def job_experience(jobs_list: [list[Param]]):
    m = InlineKeyboardMarkup()
    for jobs in jobs_list:
        job_name = f"✔️{jobs.param_title}" if jobs.is_enabled else jobs.param_title
        m.add(InlineKeyboardButton(job_name, callback_data=f'job-switch_{jobs.internal_id}'))
    m.add(InlineKeyboardButton('📧Отправить выбор', callback_data='job-finish'))
    return m


def relationship_markup():
    m = InlineKeyboardMarkup()
    m.add(InlineKeyboardButton('🕴️Холост', callback_data='relationship-single'))
    m.insert(InlineKeyboardButton('🧑‍🤝‍🧑В отношениях', callback_data='relationship-pair'))
    return m


def bad_habits(habits_list: [list[Param]]):
    m = InlineKeyboardMarkup()
    for habit in habits_list:
        habit_name = f"✔️{habit.param_title}" if habit.is_enabled else habit.param_title
        m.add(InlineKeyboardButton(habit_name, callback_data=f'habit-switch_{habit.internal_id}'))
    m.add(InlineKeyboardButton('📧Отправить выбор', callback_data='finish-habit'))
    return m


def send_phone_number():
    m = ReplyKeyboardMarkup(resize_keyboard=True)
    m.add(KeyboardButton('Отправить номер', request_contact=True))
    return m
