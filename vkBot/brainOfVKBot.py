from os import environ

from vkBot.VKontakteBot import VKontakteBot
from vkBot import markups, messages
from logger import log_this, send_mail
from database import mediator
from stuff import get_subclasses
from parserEduPage.get_timetable import get_text_timetable

token = environ.get('TOKEN_SHIT_VK')
bot = VKontakteBot(token)


def run_vk_bot():
    print('lego')
    for event in bot.longpoll.listen():
        print(event.object)
        for key in event.object:
            print(key, event.object[key])
        bot.process_event(event)


@bot.message_handler(command='Начать')
def start_message(event):
    # send_mail(event)
    bot.send_message(chat_id=event.chat_id, text=messages.START)
    bot.send_message(chat_id=event.chat_id, text=messages.REGISTRATION)
    bot.send_message(chat_id=event.chat_id, text=messages.REGISTRATION_ASK_SURNAME)
    bot.register_next_step_handler(
        chat_id=event.chat_id,
        callback=registration_ask_surname,
        information_about_student=dict(),
    )


def registration_ask_surname(event, information_about_student):
    information_about_student['surname'] = bot.get_text(event)
    bot.send_message(chat_id=event.chat_id, text=messages.REGISTRATION_ASK_NAME)
    bot.register_next_step_handler(
        chat_id=event.chat_id,
        callback=registration_ask_name,
        information_about_student=information_about_student,
    )


def registration_ask_name(event, information_about_student):
    information_about_student['name'] = bot.get_text(event)
    bot.send_message(chat_id=event.chat_id, text=messages.REGISTRATION_ASK_NUMBER_CLASS,
                     reply_markup=markups.numbers_class)
    bot.register_next_step_handler(
        chat_id=event.chat_id,
        callback=registration_ask_number_class,
        information_about_student=information_about_student,
    )


def registration_ask_number_class(event, information_about_student):
    information_about_student['number_class'] = bot.get_text(event)
    bot.send_message(chat_id=event.chat_id, text=messages.REGISTRATION_ASK_LETTER_CLASS,
                     reply_markup=markups.letters_class)
    bot.register_next_step_handler(
        chat_id=event.chat_id,
        callback=registration_ask_letter_class,
        information_about_student=information_about_student,
    )


def registration_ask_letter_class(event, information_about_student):
    information_about_student['letter_class'] = bot.get_text(event)
    bot.send_message(chat_id=event.chat_id, text=messages.REGISTRATION_ASK_SUBCLASS,
                     reply_markup=markups.get_subclasses_markup(
                         number=information_about_student['number_class'],
                         letter=information_about_student['letter_class'],
                     ))
    bot.register_next_step_handler(
        chat_id=event.chat_id,
        callback=registration_ask_subclass,
        information_about_student=information_about_student,
    )


def registration_ask_subclass(event, information_about_student):
    information_about_student['subclass'] = bot.get_text(event)
    mediator.add_student(telegram_user_id=event.chat_id, **information_about_student)
    welcoming(chat_id=event.chat_id, information_about_student=information_about_student)


def welcoming(chat_id, information_about_student):
    subclasses = get_subclasses(number=information_about_student['number_class'],
                                letter=information_about_student['letter_class'])
    another_subclass = subclasses[0] if information_about_student['subclass'] == subclasses[1] else subclasses[1]
    bot.send_message(chat_id=chat_id, reply_markup=markups.menu,
                     text=messages.WELCOME.format(**information_about_student, another_subclass=another_subclass))


@bot.message_handler(command='Настройки')
def command_settings(event):
    bot.register_next_step_handler(
        chat_id=bot.send_message(chat_id=event.chat_id, text=messages.SETTINGS_INTRODUCING,
                                 reply_markup=markups.settings),
        callback=settings
    )


def settings(event):
    text = bot.get_text(event)
    if text.lower() == 'параметры вывода':
        bot.send_message(chat_id=event.chat_id, text=messages.SETTINGS_PARAMETERS_OUTPUT,
                         reply_markup=markups.get_parameters_output_inline_markup(
                             **mediator.get_parameters_output(telegram_user_id=event.chat_id)
                         ))

    if text.lower() == 'в главное меню':
        bot.send_message(chat_id=event.chat_id, text=messages.SETTINGS_INTRODUCING,
                         reply_markup=markups.menu)


@bot.message_handler(command='скинь расписание')
def command_send_timetable(event):
    bot.register_next_step_handler(
        chat_id=bot.send_message(chat_id=event.chat_id, text=messages.SETTINGS_INTRODUCING,
                                 reply_markup=markups.choose_day_timetable),
        callback=send_timetable
    )


def send_timetable(event):
    text = bot.get_text(event)
    needed_class = '10д-ит'
    if text.lower() == 'сегодня':
        needed_date = 'today'
        text_timetable = get_text_timetable(needed_class=needed_class,
                                            needed_date=needed_date
                                            )
        bot.register_next_step_handler(
            chat_id=bot.send_message(chat_id=event.chat_id, text=text_timetable,
                                     reply_markup=markups.choose_day_timetable),
            callback=send_timetable
        )

    if text.lower() == 'завтра':
        needed_date = 'tomorrow'
        text_timetable = get_text_timetable(needed_class=needed_class,
                                            needed_date=needed_date
                                            )
        bot.register_next_step_handler(
            chat_id=bot.send_message(chat_id=event.chat_id, text=text_timetable,
                                     reply_markup=markups.choose_day_timetable),
            callback=send_timetable
        )
    if text.lower() == 'послезавтра':
        needed_date = 'after_tomorrow'
        bot.register_next_step_handler(
            chat_id=bot.send_message(chat_id=event.chat_id, text=text_timetable,
                                     reply_markup=markups.choose_day_timetable),
            callback=send_timetable
        )
    if text.lower() == 'в главное меню':
        bot.send_message(chat_id=event.chat_id, text=messages.SETTINGS_INTRODUCING,
                         reply_markup=markups.menu)

# @bot.callback_query_handler(func=lambda call: True)
# def callback_inline(call):
#     if call.data:
#         mediator.change_parameter(telegram_user_id=call.message.chat.id, parameter=call.data)
#         bot.edit_message_reply_markup(chat_id=call.message.chat.id,
#                                       message_id=call.message.message_id,
#                                       reply_markup=markups.get_parameters_output_inline_markup(
#                                           **mediator.get_parameters_output(telegram_user_id=call.message.chat.id)
#                                       ))
