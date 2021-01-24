from telebot import types

source_markup = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
source_markup_btn1 = types.KeyboardButton('Перевести текст в синонимы')
source_markup_btn2 = types.KeyboardButton('/help')
source_markup_btn3 = types.KeyboardButton('/about')
source_markup_btn4 = types.KeyboardButton('/feedback')
source_markup.add(source_markup_btn1)
source_markup.add(source_markup_btn2)
source_markup.add(source_markup_btn3)
source_markup.add(source_markup_btn4)

none_markup = types.ReplyKeyboardRemove()
