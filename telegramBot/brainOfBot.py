import telebot

from telegramBot import markups, messages
from logger import log_this
from database import mediator

# token = environ.get('TOKEN_SHIT')
import config

token = config.TOKEN
bot = telebot.TeleBot(token, parse_mode='markdown')


@bot.message_handler(commands=['start'])
@log_this
def start_message(message):
    # send_mail(message)
    bot.send_message(chat_id=message.chat.id, text=messages.START)
    bot.send_message(chat_id=message.chat.id, text=messages.REGISTRATION)
    bot.register_next_step_handler(
        message=bot.send_message(chat_id=message.chat.id, text=messages.ASK_SURNAME,
                                 reply_markup=markups.empty),
        callback=ask_surname,
        information_about_student=dict(),
    )
    # bot.send_sticker(chat_id=message.chat.id,
    # data='CAACAgIAAxkBAAM3Xx3eHjxLZMGi9GQCWRozmRovnAsAAh4DAAKNSjADcnw1sWQ7ES8aBA')


@log_this
def ask_surname(message, information_about_student):
    information_about_student['surname'] = message.text
    bot.register_next_step_handler(
        message=bot.send_message(chat_id=message.chat.id, text=messages.ASK_NAME,
                                 reply_markup=markups.empty),
        callback=ask_name,
        information_about_student=information_about_student,
    )


@log_this
def ask_name(message, information_about_student):
    information_about_student['name'] = message.text
    bot.register_next_step_handler(
        message=bot.send_message(chat_id=message.chat.id, text=messages.ASK_NUMBER_CLASS,
                                 reply_markup=markups.numbers_class),
        callback=ask_number_class,
        information_about_student=information_about_student,
    )


@log_this
def ask_number_class(message, information_about_student):
    information_about_student['number_class'] = message.text
    bot.register_next_step_handler(
        message=bot.send_message(chat_id=message.chat.id, text=messages.ASK_LETTER_CLASS,
                                 reply_markup=markups.letters_class),
        callback=ask_letter_class,
        information_about_student=information_about_student,
    )


@log_this
def ask_letter_class(message, information_about_student):
    information_about_student['letter_class'] = message.text
    bot.register_next_step_handler(
        message=bot.send_message(chat_id=message.chat.id, text=messages.ASK_SUBCLASS,
                                 reply_markup=markups.get_subclasses_markup(
                                     number=information_about_student['number_class'],
                                     letter=information_about_student['letter_class'],
                                 )),
        callback=ask_subclass,
        information_about_student=information_about_student,
    )


@log_this
def ask_subclass(message, information_about_student):
    information_about_student['subclass'] = message.text
    mediator.add_student(telegram_user_id=message.chat.id, name=information_about_student['name'])
    bot.send_message(chat_id=message.chat.id, text='Hello ' + str(information_about_student),
                     reply_markup=markups.empty)


@bot.message_handler(commands=['help'])
@log_this
def help_message(message):
    bot.send_message(chat_id=message.chat.id, text=messages.HELP, reply_markup=markups.source)


@bot.message_handler(commands=['about'])
@log_this
def about_message(message):
    bot.send_message(chat_id=message.chat.id, text=messages.ABOUT, reply_markup=markups.source)


@bot.message_handler(commands=['feedback'])
@log_this
def feedback_message(message):
    bot.send_message(chat_id=message.chat.id, text=messages.FEEDBACK, reply_markup=markups.source)


@bot.message_handler(content_types=['text'])
@log_this
def dialogue(message):
    if do_prikol(message):
        return
    if message.text.lower() == 'перевести текст в синонимы':
        msg = bot.send_message(chat_id=message.chat.id, text=messages.ASK_TEXT, reply_markup=markups.empty)
        bot.register_next_step_handler(msg, ask_text)
    else:
        print(message)
        help_message(message)


@bot.message_handler(content_types=['video_note'])
@log_this
def video(message):
    bot.send_message(chat_id=message.chat.id, text=messages.video, reply_markup=markups.source)
