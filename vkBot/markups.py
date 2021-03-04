from vk_api.keyboard import VkKeyboard, VkKeyboardColor
from stuff import get_subclasses

# source = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
# source.add(types.KeyboardButton('/feedback'))

numbers_class = VkKeyboard(one_time=False)
numbers_class.add_button('8', color=VkKeyboardColor.NEGATIVE)
numbers_class.add_button('9', color=VkKeyboardColor.POSITIVE)
numbers_class.add_line()
numbers_class.add_button('10', color=VkKeyboardColor.NEGATIVE)
numbers_class.add_button('11', color=VkKeyboardColor.POSITIVE)

letters_class = VkKeyboard(one_time=False)
letters_class.add_button('А', color=VkKeyboardColor.NEGATIVE)
letters_class.add_button('Б', color=VkKeyboardColor.POSITIVE)
letters_class.add_line()
letters_class.add_button('В', color=VkKeyboardColor.NEGATIVE)
letters_class.add_button('Г', color=VkKeyboardColor.POSITIVE)
letters_class.add_line()
letters_class.add_button('Д', color=VkKeyboardColor.PRIMARY)


def get_subclasses_markup(number: str, letter: str):
    tmp_markup = VkKeyboard(one_time=False)
    subclasses = get_subclasses(number=number, letter=letter)
    tmp_markup.add_button(subclasses[0])
    tmp_markup.add_line()
    tmp_markup.add_button(subclasses[1])
    return tmp_markup


menu = VkKeyboard(one_time=False)
menu.add_button('Скинь расписание')
menu.add_line()
menu.add_button('Покажи время до конца пары')
menu.add_line()
menu.add_button('Настройки')
menu.add_line()
menu.add_button('О боте')

settings = VkKeyboard(one_time=False)
settings.add_button('Параметры вывода')
settings.add_line()
settings.add_button('Изменить список классов')
settings.add_line()
settings.add_button('Настроить время отправки расписания')
settings.add_line()
settings.add_button('В главное меню')

choose_day_timetable = VkKeyboard(one_time=False)
choose_day_timetable.add_button('Сегодня')
choose_day_timetable.add_line()
choose_day_timetable.add_button('Завтра')
choose_day_timetable.add_line()
choose_day_timetable.add_button('Послезавтра')
choose_day_timetable.add_line()
choose_day_timetable.add_button('В главное меню')


def get_user_classes_markup(classes):
    tmp_markup = VkKeyboard(one_time=False)
    i = 0
    for i, (number, letter, subclass) in enumerate(classes):
        tmp_markup.add_button(f'{number}{letter}-{subclass}'.lower(), color=VkKeyboardColor.PRIMARY)
        if i != len(classes) - 1:
            tmp_markup.add_line()
    return tmp_markup


parameters_output_markup = VkKeyboard(one_time=False)

button_start_lesson_text = 'Начало урока'
button_end_lesson_text = 'Конец урока'
button_room_number_text = 'Номер кабинета'
button_teacher_name_text = 'Имя учителя'
button_subject_text = 'Название предмета'

parameters_output_markup.add_button(button_start_lesson_text)
parameters_output_markup.add_line()
parameters_output_markup.add_button(button_end_lesson_text)
parameters_output_markup.add_line()
parameters_output_markup.add_button(button_room_number_text)
parameters_output_markup.add_line()
parameters_output_markup.add_button(button_teacher_name_text)
parameters_output_markup.add_line()
parameters_output_markup.add_button(button_subject_text)
parameters_output_markup.add_line()
parameters_output_markup.add_button('В главное меню')