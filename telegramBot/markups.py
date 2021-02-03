from telebot import types
from stuff import get_subclasses

source = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
source.add(types.KeyboardButton('/feedback'))

numbers_class = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
numbers_class.add('8', '9',
                  '10', '11',
                  )

letters_class = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
letters_class.add('А', 'Б',
                  'В', 'Г',
                  'Д',
                  )


def get_subclasses_markup(number: str, letter: str):
    tmp_markup = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    subclasses = get_subclasses(number=number, letter=letter)
    tmp_markup.add(*subclasses)
    return tmp_markup


menu = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
menu.add('Скинь расписание',
         'Покажи время до конца пары',
         'Настройки',
         'О боте',
         )

settings = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
settings.add('Параметры вывода',
             'Изменить список классов',
             'Настроить время отправки расписания',
             'В главное меню',
             )


def get_user_classes_markup(*classes):
    tmp_markup = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    print(*classes)
    for number, letter, subclass in *classes:
        print(number, letter, subclass)
        tmp_markup.add(f'{number}{letter}-{subclass}'.lower())
    return tmp_markup


def get_parameters_output_inline_markup(start_lesson: bool = True,
                                        end_lesson: bool = True,
                                        room_number: bool = True,
                                        teacher_name: bool = True,
                                        subject: bool = True):
    is_chosen = '🟢'
    is_not_chosen = '🔴'
    tmp_markup = types.InlineKeyboardMarkup(row_width=1)

    is_chosen_element = is_chosen if start_lesson else is_not_chosen
    button_start_lesson = types.InlineKeyboardButton(
        text=f'{is_chosen_element} Начало урока {is_chosen_element}',
        callback_data='CHANGE_OUTPUT start lesson')

    is_chosen_element = is_chosen if end_lesson else is_not_chosen
    button_end_lesson = types.InlineKeyboardButton(
        text=f'{is_chosen_element} Конец урока {is_chosen_element}',
        callback_data='CHANGE_OUTPUT end lesson')

    is_chosen_element = is_chosen if room_number else is_not_chosen
    button_room_number = types.InlineKeyboardButton(
        text=f'{is_chosen_element} Номер кабинета {is_chosen_element}',
        callback_data='CHANGE_OUTPUT room number')

    is_chosen_element = is_chosen if teacher_name else is_not_chosen
    button_teacher_name = types.InlineKeyboardButton(
        text=f'{is_chosen_element} Имя учителя {is_chosen_element}',
        callback_data='CHANGE_OUTPUT teacher name')

    is_chosen_element = is_chosen if subject else is_not_chosen
    button_subject = types.InlineKeyboardButton(
        text=f'{is_chosen_element} Название предмета {is_chosen_element}',
        callback_data='CHANGE_OUTPUT subject')

    tmp_markup.add(button_start_lesson, button_end_lesson, button_room_number, button_subject, button_teacher_name)
    tmp_markup.add(types.InlineKeyboardButton(text='В главное меню', callback_data='CHANGE_OUTPUT menu'))
    return tmp_markup


def get_dates_inline_markup(needed_class):
    tmp_markup = types.InlineKeyboardMarkup(row_width=1)
    button_yesterday = types.InlineKeyboardButton(
        text=f'Вчера',
        callback_data=f'ASK_DATE yesterday {needed_class}')
    button_today = types.InlineKeyboardButton(
        text=f'Сегодня',
        callback_data=f'ASK_DATE today {needed_class}')
    button_tomorrow = types.InlineKeyboardButton(
        text=f'Завтра',
        callback_data=f'ASK_DATE tomorrow {needed_class}')
    button_after_tomorrow = types.InlineKeyboardButton(
        text=f'Послезавтра',
        callback_data=f'ASK_DATE after_tomorrow {needed_class}')
    button_more_day = types.InlineKeyboardButton(
        text=f'Больше дней',
        callback_data=f'ASK_DATE more_day {needed_class}')
    tmp_markup.add(button_yesterday, button_today, button_tomorrow, button_after_tomorrow, button_more_day)
    tmp_markup.add(types.InlineKeyboardButton(text='В главное меню', callback_data='ASK_DATE menu'))
    return tmp_markup


empty = types.ReplyKeyboardRemove()
