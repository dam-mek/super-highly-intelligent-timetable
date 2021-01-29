import telebot
from os import environ

from telegramBot import markups, messages
from logger import log_this, send_mail
from database import mediator
from stuff import get_subclasses

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


@bot.message_handler(content_types=['text'])
@log_this
def dialogue(message):
    if message.text.lower() == 'настройки':
        bot.register_next_step_handler(
            message=bot.send_message(chat_id=message.chat.id, text=messages.SETTINGS_INTRODUCING,
                                     reply_markup=markups.settings),
            callback=settings
        )
    else:
        print(message)


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
    if call.data:
        mediator.change_parameter(telegram_user_id=call.message.chat.id, parameter=call.data)
        bot.edit_message_reply_markup(chat_id=call.message.chat.id,
                                      message_id=call.message.message_id,
                                      reply_markup=markups.get_parameters_output_inline_markup(
                                          **mediator.get_parameters_output(telegram_user_id=call.message.chat.id)
                                      ))


@bot.message_handler(content_types=['video_note'])
@log_this
def video(message):
    bot.send_message(chat_id=message.chat.id, text=messages.video, reply_markup=markups.menu)
