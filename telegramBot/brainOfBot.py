from telegramBot import markups, messages
from logger import log_this

import telebot

# token = environ.get('TOKEN_AMB')
import config

token = config.TOKEN
bot = telebot.TeleBot(token, parse_mode='markdown')


@bot.message_handler(commands=['start'])
@log_this
def start_message(message):
    # send_mail(message)
    bot.send_message(chat_id=message.chat.id, text=messages.START, reply_markup=markups.source_markup)
    # bot.send_sticker(chat_id=message.chat.id,
    # data='CAACAgIAAxkBAAM3Xx3eHjxLZMGi9GQCWRozmRovnAsAAh4DAAKNSjADcnw1sWQ7ES8aBA')


@bot.message_handler(commands=['help'])
@log_this
def help_message(message):
    bot.send_message(chat_id=message.chat.id, text=messages.HELP, reply_markup=markups.source_markup)


@bot.message_handler(commands=['about'])
@log_this
def about_message(message):
    bot.send_message(chat_id=message.chat.id, text=messages.ABOUT, reply_markup=markups.source_markup)


@bot.message_handler(commands=['feedback'])
@log_this
def feedback_message(message):
    bot.send_message(chat_id=message.chat.id, text=messages.FEEDBACK, reply_markup=markups.source_markup)


@bot.message_handler(content_types=['text'])
@log_this
def dialogue(message):
    if do_prikol(message):
        return
    if message.text.lower() == 'перевести текст в синонимы':
        msg = bot.send_message(chat_id=message.chat.id, text=messages.ASK_TEXT, reply_markup=markups.none_markup)
        bot.register_next_step_handler(msg, ask_text)
    else:
        print(message)
        help_message(message)


@bot.message_handler(content_types=['video_note'])
@log_this
def video(message):
    bot.send_message(chat_id=message.chat.id, text=messages.video, reply_markup=markups.source_markup)


def ask_text(message):
    if message.text is None:
        msg = bot.send_message(chat_id=message.chat.id, text=messages.ASK_EXACTLY_TEXT, parse_mode='markdown')
        bot.register_next_step_handler(msg, ask_text)
        return
    msg = bot.send_message(chat_id=message.chat.id, text='Сделано: *0%*', parse_mode='markdown')
    generator_text = parserSynonym.main(message.text)
    text = next(generator_text)
    while type(text) is int:
        text_tmp = next(generator_text)
        while text_tmp == text:
            text_tmp = next(generator_text)
        text = text_tmp
        bot.edit_message_text(chat_id=message.chat.id, message_id=msg.message_id, text=f'Сделано: *{text}%*')
    bot.delete_message(chat_id=message.chat.id, message_id=msg.message_id)
    bot.send_message(chat_id=message.chat.id, text=text,
                     reply_markup=markups.source_markup)
    # with open('log.log', 'a') as file:
    #     file.write(f'RESULT:MSG_ID-{message.message_id}:{text}\n')


def do_prikol(msg):
    """
    It will do prikol. Return True if prikol can exist

    :param msg: <class 'telebot.types.Message'>
    :return: bool
    """
    text = msg.text.lower()
    if text in {'suck', 'пососи'}:
        bot.send_message(msg.chat.id, messages.suck)
    elif text in {'кадиллак', 'кадилак', 'cadillac', 'cadilac'}:
        bot.send_message(msg.chat.id, messages.cadillac)
    elif text in {'baby', 'малышка'}:
        bot.send_message(msg.chat.id, messages.baby)
    elif text in {'ice', 'лед', 'лёд', 'айс'}:
        bot.send_message(msg.chat.id, messages.ice)
    elif text in {'плодотворная дебютная идея'}:
        bot.send_message(msg.chat.id, messages.ostap)
    else:
        return False
    return True
