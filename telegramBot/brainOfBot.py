import telebot
from os import environ
import datetime
import pytz
import calendar

from telegramBot import markups, messages
from logger import log_this, send_mail
from database import mediator
from stuff import get_subclasses, School_class
from parserEduPage import get_timetable

timezone = pytz.timezone('Etc/GMT-7')

token = environ.get('TOKEN_SHIT')
bot = telebot.TeleBot(token, parse_mode='markdown')


@bot.message_handler(commands=['start'])
@log_this
def start_message(message):
    send_mail(message)
    bot.send_message(chat_id=message.chat.id, text=messages.START)
    bot.send_message(chat_id=message.chat.id, text=messages.REGISTRATION)
    bot.register_next_step_handler(
        message=bot.send_message(chat_id=message.chat.id, text=messages.REGISTRATION_ASK_SURNAME,
                                 reply_markup=markups.empty),
        callback=registration_ask_surname,
        information_about_student=dict(),
    )
    # bot.send_sticker(chat_id=message.chat.id,
    # data='CAACAgIAAxkBAAM3Xx3eHjxLZMGi9GQCWRozmRovnAsAAh4DAAKNSjADcnw1sWQ7ES8aBA')


@log_this
def registration_ask_surname(message, information_about_student):
    information_about_student['surname'] = message.text
    bot.register_next_step_handler(
        message=bot.send_message(chat_id=message.chat.id, text=messages.REGISTRATION_ASK_NAME,
                                 reply_markup=markups.empty),
        callback=registration_ask_name,
        information_about_student=information_about_student,
    )


@log_this
def registration_ask_name(message, information_about_student):
    information_about_student['name'] = message.text
    bot.register_next_step_handler(
        message=bot.send_message(chat_id=message.chat.id, text=messages.REGISTRATION_ASK_NUMBER_CLASS,
                                 reply_markup=markups.numbers_class),
        callback=registration_ask_number_class,
        information_about_student=information_about_student,
    )


@log_this
def registration_ask_number_class(message, information_about_student):
    information_about_student['number_class'] = message.text
    bot.register_next_step_handler(
        message=bot.send_message(chat_id=message.chat.id, text=messages.REGISTRATION_ASK_LETTER_CLASS,
                                 reply_markup=markups.letters_class),
        callback=registration_ask_letter_class,
        information_about_student=information_about_student,
    )


@log_this
def registration_ask_letter_class(message, information_about_student):
    information_about_student['letter_class'] = message.text
    bot.register_next_step_handler(
        message=bot.send_message(chat_id=message.chat.id, text=messages.REGISTRATION_ASK_SUBCLASS,
                                 reply_markup=markups.get_subclasses_markup(
                                     number=information_about_student['number_class'],
                                     letter=information_about_student['letter_class'],
                                 )),
        callback=registration_ask_subclass,
        information_about_student=information_about_student,
    )


@log_this
def registration_ask_subclass(message, information_about_student):
    information_about_student['subclass'] = message.text
    mediator.add_student(telegram_user_id=message.chat.id, **information_about_student)
    welcoming(telegram_user_id=message.chat.id, information_about_student=information_about_student)


def welcoming(telegram_user_id, information_about_student):
    subclasses = get_subclasses(number=information_about_student['number_class'],
                                letter=information_about_student['letter_class'])
    another_subclass = subclasses[0] if information_about_student['subclass'] == subclasses[1] else subclasses[1]
    bot.send_message(chat_id=telegram_user_id, reply_markup=markups.menu,
                     text=messages.WELCOME.format(**information_about_student, another_subclass=another_subclass))


@bot.message_handler(commands=['settings'])
@log_this
def command_settings(message):
    bot.register_next_step_handler(
        message=bot.send_message(chat_id=message.chat.id, text=messages.SETTINGS_INTRODUCING,
                                 reply_markup=markups.settings),
        callback=settings
    )


@bot.message_handler(commands=['menu'])
@log_this
def command_settings(message):
    bot.send_message(chat_id=message.chat.id, text=messages.MENU,
                     reply_markup=markups.menu),


@bot.message_handler(content_types=['text'])
@log_this
def dialogue(message):
    if message.text.lower() == 'скинь расписание':
        ask_user_class(message)
    elif message.text.lower() == 'настройки':
        bot.register_next_step_handler(
            message=bot.send_message(chat_id=message.chat.id, text=messages.SETTINGS_INTRODUCING,
                                     reply_markup=markups.settings),
            callback=settings
        )
    else:
        print(message)


@log_this
def ask_user_class(message):
    user_classes = mediator.get_user_classes(telegram_user_id=message.chat.id)
    if len(user_classes) == 1:
        ask_needed_class(message, user_classes)
    else:
        classes_markup = markups.get_user_classes_markup(*user_classes)
        bot.register_next_step_handler(
            message=bot.send_message(chat_id=message.chat.id, text=messages.SENDING_TIMETABLE_ASK_USER_CLASS,
                                     reply_markup=classes_markup),
            callback=ask_needed_class,
            user_classes=user_classes
        )


@log_this
def ask_needed_class(message, user_classes):
    if len(user_classes) == 1:
        needed_class = user_classes[0]
    else:
        needed_class = message.text
    print(needed_class)
    needed_class = School_class(number=needed_class[0], letter=needed_class[1], subclass=needed_class[2])
    print(needed_class)

    bot.send_message(chat_id=message.chat.id, text=messages.SENDING_TIMETABLE_ASK_DATE,
                     reply_markup=markups.get_dates_inline_markup(needed_class=needed_class))


def send_timetable(telegram_user_id, needed_class, needed_date):
    changing_date = {
        'yesterday': -1,
        'today': 0,
        'tomorrow': 1,
        'after_tomorrow': 2,
    }
    print(needed_class)
    needed_date = datetime.datetime.now(timezone).date() + datetime.timedelta(days=changing_date[needed_date])
    timetable = get_timetable.get_timetable(needed_class=needed_class,
                                            day=str(needed_date.day),
                                            month=str(needed_date.month),
                                            )
    weekend = {
        0: 'Понедельник',
        1: 'Вторник',
        2: 'Среда',
        3: 'Четверг',
        4: 'Пятница',
        5: 'Суббота',
        6: 'Воскресенье',
    }

    day_in_week = calendar.weekday(year=2021, month=needed_date.month, day=needed_date.day)

    timetable_text = f"{needed_date.strftime('%d.%m.%y')} {weekend[day_in_week]} {needed_class.upper()}\n\n"
    for subject in sorted(timetable, key=lambda info: datetime.datetime.strptime(info['startLesson'], '%H:%M')):
        if 'startLesson' in subject:
            timetable_text += f"""{subject['startLesson']}"""
            if 'endLesson' in subject:
                timetable_text += f"""-"""
        if 'endLesson' in subject:
            timetable_text += f"""{subject['endLesson']}"""
        if 'endLesson' or 'startLesson' in subject:
            timetable_text += f""": """
        if 'subject' in subject:
            timetable_text += f"""{subject['subject'].lower()} """
        if 'teacherName' in subject:
            timetable_text += f"""{subject['teacherName']} """
        if 'teacherName' in subject:
            timetable_text += f"""(каб. {subject['roomNumber']})"""
        timetable_text += '\n'

    bot.send_message(chat_id=telegram_user_id, text=timetable_text, reply_markup=markups.menu)


@log_this
def settings(message):
    if message.text.lower() == 'параметры вывода':
        bot.send_message(chat_id=message.chat.id, text=messages.SETTINGS_PARAMETERS_OUTPUT,
                         reply_markup=markups.get_parameters_output_inline_markup(
                             **mediator.get_parameters_output(telegram_user_id=message.chat.id)
                         ))

    if message.text.lower() == 'в главное меню':
        bot.send_message(chat_id=message.chat.id, text=messages.SETTINGS_INTRODUCING,
                         reply_markup=markups.menu)


@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    command = call.data.split()[0]
    if command == 'CHANGE_OUTPUT':
        mediator.change_parameter(telegram_user_id=call.message.chat.id, parameter=call.data)
        bot.edit_message_reply_markup(chat_id=call.message.chat.id,
                                      message_id=call.message.message_id,
                                      reply_markup=markups.get_parameters_output_inline_markup(
                                          **mediator.get_parameters_output(telegram_user_id=call.message.chat.id)
                                      ))
    if command == 'ASK_DATE':
        print(call.data)
        command, needed_date, needed_class = call.data.split()
        if needed_class == 'more_day':
            bot.edit_message_reply_markup(chat_id=call.message.chat.id,
                                          message_id=call.message.message_id,
                                          reply_markup=markups.get_parameters_output_inline_markup(
                                              **mediator.get_parameters_output(telegram_user_id=call.message.chat.id)
                                          ))
        else:
            send_timetable(telegram_user_id=call.message.chat.id, needed_class=needed_class, needed_date=needed_date)


@bot.message_handler(content_types=['video_note'])
@log_this
def video(message):
    bot.send_message(chat_id=message.chat.id, text=messages.video, reply_markup=markups.menu)
