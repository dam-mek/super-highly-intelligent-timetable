from os import environ

from vkBot.VKontakteBot import VKontakteBot
from vkBot import markups, messages
from logger import log_this, send_mail
from database import mediator
from stuff import get_subclasses, Group
from parserEduPage.get_timetable import get_text_timetable

token = environ.get('TOKEN_SHIT_VK')
bot = VKontakteBot(token)


@bot.message_handler(command='Начать')
def start_message(event):
    # send_mail(event)
    bot.send_message(chat_id=event['peer_id'], text=messages.START)
    bot.send_message(chat_id=event['peer_id'], text=messages.REGISTRATION)
    bot.send_message(chat_id=event['peer_id'], text=messages.REGISTRATION_ASK_SURNAME)
    bot.register_next_step_handler(
        chat_id=event['peer_id'],
        callback=registration_ask_surname,
        information_about_student=dict(),
    )


def registration_ask_surname(event, information_about_student):
    information_about_student['surname'] = bot.get_text(event)
    bot.send_message(chat_id=event['peer_id'], text=messages.REGISTRATION_ASK_NAME)
    bot.register_next_step_handler(
        chat_id=event['peer_id'],
        callback=registration_ask_name,
        information_about_student=information_about_student,
    )


def registration_ask_name(event, information_about_student):
    information_about_student['name'] = bot.get_text(event)
    bot.send_message(chat_id=event['peer_id'], text=messages.REGISTRATION_ASK_NUMBER_CLASS,
                     reply_markup=markups.numbers_class)
    bot.register_next_step_handler(
        chat_id=event['peer_id'],
        callback=registration_ask_number_class,
        information_about_student=information_about_student,
    )


def registration_ask_number_class(event, information_about_student):
    information_about_student['number_class'] = bot.get_text(event)
    bot.send_message(chat_id=event['peer_id'], text=messages.REGISTRATION_ASK_LETTER_CLASS,
                     reply_markup=markups.letters_class)
    bot.register_next_step_handler(
        chat_id=event['peer_id'],
        callback=registration_ask_letter_class,
        information_about_student=information_about_student,
    )


def registration_ask_letter_class(event, information_about_student):
    information_about_student['letter_class'] = bot.get_text(event)
    bot.send_message(chat_id=event['peer_id'], text=messages.REGISTRATION_ASK_SUBCLASS,
                     reply_markup=markups.get_subclasses_markup(
                         number=information_about_student['number_class'],
                         letter=information_about_student['letter_class'],
                     ))
    bot.register_next_step_handler(
        chat_id=event['peer_id'],
        callback=registration_ask_subclass,
        information_about_student=information_about_student,
    )


def registration_ask_subclass(event, information_about_student):
    information_about_student['subclass'] = bot.get_text(event)
    mediator.add_student(telegram_user_id=event['peer_id'], **information_about_student)
    welcoming(chat_id=event['peer_id'], information_about_student=information_about_student)


def welcoming(chat_id, information_about_student):
    subclasses = get_subclasses(number=information_about_student['number_class'],
                                letter=information_about_student['letter_class'])
    another_subclass = subclasses[0] if information_about_student['subclass'] == subclasses[1] else subclasses[1]
    bot.send_message(chat_id=chat_id, reply_markup=markups.menu,
                     text=messages.WELCOME.format(**information_about_student, another_subclass=another_subclass))


@bot.message_handler(command='Настройки')
def command_settings(event):
    bot.register_next_step_handler(
        chat_id=bot.send_message(chat_id=event['peer_id'], text=messages.SETTINGS_INTRODUCING,
                                 reply_markup=markups.settings),
        callback=settings
    )


def settings(event):
    text = bot.get_text(event)
    if text.lower() == 'параметры вывода':
        bot.send_message(chat_id=event['peer_id'], text=messages.SETTINGS_PARAMETERS_OUTPUT,
                         reply_markup=markups.get_parameters_output_inline_markup(
                             **mediator.get_parameters_output(telegram_user_id=event['peer_id'])
                         ))

    if text.lower() == 'в главное меню':
        bot.send_message(chat_id=event['peer_id'], text=messages.SETTINGS_INTRODUCING,
                         reply_markup=markups.menu)


@bot.message_handler(command='скинь расписание')
def command_send_timetable(event):
    ask_user_class(event)
    # bot.register_next_step_handler(
    #     chat_id=bot.send_message(chat_id=event['peer_id'], text=messages.SETTINGS_INTRODUCING,
    #                              reply_markup=markups.choose_day_timetable),
    #     callback=send_timetable
    # )


def ask_user_class(event):
    user_classes = mediator.get_user_classes(user_id=event['peer_id'])
    if len(user_classes) == 1:
        ask_needed_class(event, user_classes)
    else:
        classes_markup = markups.get_user_classes_markup(user_classes)
        bot.register_next_step_handler(
            chat_id=bot.send_message(chat_id=event['peer_id'], text=messages.SENDING_TIMETABLE_ASK_USER_CLASS,
                                     reply_markup=classes_markup),
            callback=ask_needed_class,
            user_classes=user_classes
        )


def ask_needed_class(event, user_classes):
    if len(user_classes) == 1:
        needed_class = user_classes[0]
    else:
        number_class, subclass = bot.get_text(event).split('-')
        needed_class = [number_class[:-1], number_class[-1:], subclass]
    needed_class = Group(number=needed_class[0], letter=needed_class[1], subclass=needed_class[2])
    bot.register_next_step_handler(
        chat_id=bot.send_message(chat_id=event['peer_id'], text=messages.SENDING_TIMETABLE_ASK_DATE,
                                 reply_markup=markups.choose_day_timetable),
        callback=send_timetable,
        needed_class=needed_class,
    )


def send_timetable(event, needed_class):
    text = bot.get_text(event).lower()
    if text == 'в главное меню':
        bot.send_message(chat_id=event['peer_id'], text=messages.SETTINGS_INTRODUCING,
                         reply_markup=markups.menu)
        return

    if text == 'сегодня':
        needed_date = 'today'
    elif text == 'завтра':
        needed_date = 'tomorrow'
    elif text == 'послезавтра':
        needed_date = 'after_tomorrow'
    else:
        needed_date = 'today'

    text_timetable = get_text_timetable(needed_class=needed_class,
                                        needed_date=needed_date
                                        )
    chat_id = bot.send_message(chat_id=event['peer_id'], text=text_timetable,
                               reply_markup=markups.menu)
    # bot.register_next_step_handler(
    #     chat_id=chat_id,
    #     callback=send_timetable,
    #     needed_date=needed_date,
    # )

# @bot.callback_query_handler(func=lambda call: True)
# def callback_inline(call):
#     if call.data:
#         mediator.change_parameter(telegram_user_id=call.message.chat.id, parameter=call.data)
#         bot.edit_message_reply_markup(chat_id=call.message.chat.id,
#                                       message_id=call.message.message_id,
#                                       reply_markup=markups.get_parameters_output_inline_markup(
#                                           **mediator.get_parameters_output(telegram_user_id=call.message.chat.id)
#                                       ))
