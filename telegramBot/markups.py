from telebot import types
from stuff import get_subclasses


source = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
source.add(types.KeyboardButton('/feedback'))

numbers_class = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
numbers_class.add(types.KeyboardButton('8'))
numbers_class.add(types.KeyboardButton('9'))
numbers_class.add(types.KeyboardButton('10'))
numbers_class.add(types.KeyboardButton('11'))

letters_class = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
letters_class.add(types.KeyboardButton('А'))
letters_class.add(types.KeyboardButton('Б'))
letters_class.add(types.KeyboardButton('В'))
letters_class.add(types.KeyboardButton('Г'))
letters_class.add(types.KeyboardButton('Д'))


none_markup = types.ReplyKeyboardRemove()
