from os import environ

from vkBot.VKontakteBot import VKontakteBot
from vkBot import markups, messages
from stuff import get_subclasses, Group, Student
from parserEduPage.get_timetable import get_text_timetable
from database import databaseAgent
from logger import log_this, send_mail

token = environ.get('TOKEN_SHIT_VK')
bot = VKontakteBot(token)


@bot.message_handler(command='Начать')
def start_message(event):
    # send_mail(event)
    chat_id = bot.get_chat_id(event)
    bot.send_message(chat_id=chat_id, text=messages.START)
    bot.send_message(chat_id=chat_id, text=messages.REGISTRATION)
    bot.send_message(chat_id=chat_id, text=messages.REGISTRATION_ASK_SURNAME)
    bot.register_next_step_handler(
        chat_id=chat_id,
        callback=registration_ask_surname,
        information_about_student=dict(),
    )


def registration_ask_surname(event, information_about_student):
    information_about_student['surname'] = bot.get_text(event)
    chat_id = bot.get_chat_id(event)
    bot.send_message(chat_id=chat_id, text=messages.REGISTRATION_ASK_NAME)
    bot.register_next_step_handler(
        chat_id=chat_id,
        callback=registration_ask_name,
        information_about_student=information_about_student,
    )


def registration_ask_name(event, information_about_student):
    information_about_student['name'] = bot.get_text(event)
    chat_id = bot.get_chat_id(event)
    bot.send_message(chat_id=chat_id, text=messages.REGISTRATION_ASK_NUMBER_CLASS,
                     reply_markup=markups.numbers_class)
    bot.register_next_step_handler(
        chat_id=chat_id,
        callback=registration_ask_number_class,
        information_about_student=information_about_student,
    )


def registration_ask_number_class(event, information_about_student):
    information_about_student['number_group'] = bot.get_text(event)
    chat_id = bot.get_chat_id(event)
    bot.send_message(chat_id=chat_id, text=messages.REGISTRATION_ASK_LETTER_CLASS,
                     reply_markup=markups.letters_class)
    bot.register_next_step_handler(
        chat_id=chat_id,
        callback=registration_ask_letter_class,
        information_about_student=information_about_student,
    )


def registration_ask_letter_class(event, information_about_student):
    information_about_student['letter_group'] = bot.get_text(event)
    chat_id = bot.get_chat_id(event)
    bot.send_message(chat_id=chat_id, text=messages.REGISTRATION_ASK_SUBCLASS,
                     reply_markup=markups.get_subclasses_markup(
                         number=information_about_student['number_group'],
                         letter=information_about_student['letter_group'],
                     ))
    bot.register_next_step_handler(
        chat_id=chat_id,
        callback=registration_ask_subclass,
        information_about_student=information_about_student,
    )


def registration_ask_subclass(event, information_about_student):
    information_about_student['subclass'] = bot.get_text(event)
    chat_id = bot.get_chat_id(event)
    student = Student(user_id=chat_id, 
                      name=information_about_student['name'],
                      surname=information_about_student['surname'])
    group = Group(number=information_about_student['number_group'],
                  letter=information_about_student['letter_group'],
                  subclass=information_about_student['subclass'])
    databaseAgent.add_student(student=student, group=group)
    welcoming(chat_id=chat_id, information_about_student=information_about_student)


def welcoming(chat_id, information_about_student):
    subclasses = get_subclasses(number=information_about_student['number_group'],
                                letter=information_about_student['letter_group'])
    another_subclass = subclasses[0] if information_about_student['subclass'] == subclasses[1] else subclasses[1]
    bot.send_message(chat_id=chat_id, reply_markup=markups.menu,
                     text=messages.WELCOME.format(**information_about_student, another_subclass=another_subclass))


@bot.message_handler(command='Настройки')
def command_settings(event):
    chat_id = bot.get_chat_id(event)
    bot.register_next_step_handler(
        chat_id=bot.send_message(chat_id=chat_id, text=messages.SETTINGS_INTRODUCING,
                                 reply_markup=markups.settings),
        callback=settings
    )


def settings(event):
    text = bot.get_text(event).lower()
    chat_id = bot.get_chat_id(event)
    if text.lower() == 'параметры вывода':
        output_parameters = databaseAgent.get_output_parameters(student_id=chat_id)
        message_text = messages.SETTINGS_PARAMETERS_OUTPUT.format(
            start_lesson='🟢' if output_parameters['start_lesson'] else '🔴',
            end_lesson='🟢' if output_parameters['end_lesson'] else '🔴',
            room_number='🟢' if output_parameters['room_number'] else '🔴',
            teacher_name='🟢' if output_parameters['teacher_name'] else '🔴',
            subject='🟢' if output_parameters['subject'] else '🔴',
        )
        bot.send_message(chat_id=chat_id, text=messages.SETTINGS_PARAMETERS_OUTPUT,
                         reply_markup=markups.parameters_output_markup)
        bot.register_next_step_handler(
            chat_id=chat_id,
            callback=change_output_parameter,
            output_parameters=output_parameters,
        )

    if text.lower() == 'в главное меню':
        bot.send_message(chat_id=chat_id, text=messages.SETTINGS_INTRODUCING,
                         reply_markup=markups.menu)


def change_output_parameter(event, output_parameters):
    text = bot.get_text(event).lower()
    chat_id = bot.get_chat_id(event)
    if text == 'в главное меню':
        databaseAgent.change_output_parameters(student_id=chat_id, new_parameters=output_parameters)
        bot.send_message(chat_id=chat_id, text=messages.SETTINGS_INTRODUCING,
                         reply_markup=markups.menu)
        return
    text = text[2:-2]
    if text == 'начало урока':
        output_parameters['start_lesson'] = not output_parameters['start_lesson']
        message_text = f'Вывод начала урока ' + 'включен' if output_parameters['start_lesson'] else 'отключен'
    elif text == 'конец урока':
        output_parameters['end_lesson'] = not output_parameters['end_lesson']
        message_text = f'Вывод конца урока ' + 'включен' if output_parameters['end_lesson'] else 'отключен'
    elif text == 'номер кабинета':
        output_parameters['room_number'] = not output_parameters['room_number']
        message_text = f'Вывод номера кабинета ' + 'включен' if output_parameters['room_number'] else 'отключен'
    elif text == 'имя учителя':
        output_parameters['teacher_name'] = not output_parameters['teacher_name']
        message_text = f'Вывод имя учителя ' + 'включен' if output_parameters['teacher_name'] else 'отключен'
    elif text == 'название предмета':
        output_parameters['subject'] = not output_parameters['subject']
        message_text = f'Вывод названия предмета ' + 'включен' if output_parameters['subject'] else 'отключен'
    else:
        problem_request(event)
        return
    bot.send_message(chat_id=chat_id, text=message_text,
                     reply_markup=markups.parameters_output_markup)
    bot.register_next_step_handler(
        chat_id=chat_id,
        callback=change_output_parameter,
        output_parameters=output_parameters,
    )
    

@bot.message_handler(command='скинь расписание')
def command_send_timetable(event):
    ask_user_class(event)
    # bot.register_next_step_handler(
    #     chat_id=bot.send_message(chat_id=chat_id, text=messages.SETTINGS_INTRODUCING,
    #                              reply_markup=markups.choose_day_timetable),
    #     callback=send_timetable
    # )


def ask_user_class(event):
    chat_id = bot.get_chat_id(event)
    user_classes = databaseAgent.get_student_groups(student_id=chat_id)
    if len(user_classes) == 1:
        ask_needed_class(event, user_classes)
    else:
        classes_markup = markups.get_user_classes_markup(user_classes)
        bot.register_next_step_handler(
            chat_id=bot.send_message(chat_id=chat_id, text=messages.SENDING_TIMETABLE_ASK_USER_CLASS,
                                     reply_markup=classes_markup),
            callback=ask_needed_class,
            user_classes=user_classes
        )


def ask_needed_class(event, user_classes):
    chat_id = bot.get_chat_id(event)
    if len(user_classes) == 1:
        needed_class = user_classes[0]
    else:
        number_class, subclass = bot.get_text(event).split('-')
        needed_class = [number_class[:-1], number_class[-1:], subclass]
    needed_class = Group(number=needed_class[0], letter=needed_class[1], subclass=needed_class[2])
    bot.register_next_step_handler(
        chat_id=bot.send_message(chat_id=chat_id, text=messages.SENDING_TIMETABLE_ASK_DATE,
                                 reply_markup=markups.choose_day_timetable),
        callback=send_timetable,
        needed_class=needed_class,
    )


def send_timetable(event, needed_class):
    text = bot.get_text(event).lower()
    chat_id = bot.get_chat_id(event)
    if text == 'в главное меню':
        bot.send_message(chat_id=chat_id, text=messages.SETTINGS_INTRODUCING,
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
                                        needed_date=needed_date,
                                        output_parameters=databaseAgent.get_output_parameters(student_id=chat_id))
    chat_id = bot.send_message(chat_id=chat_id, text=text_timetable,
                               reply_markup=markups.menu)
    # bot.register_next_step_handler(
    #     chat_id=chat_id,
    #     callback=send_timetable,
    #     needed_date=needed_date,
    # )


@bot.message_handler(command='')
def problem_request(event):
    chat_id = bot.get_chat_id(event)
    bot.send_message(chat_id=chat_id, reply_markup=markups.menu, text=messages.PROBLEM_REQUEST)

# @bot.callback_query_handler(func=lambda call: True)
# def callback_inline(call):
#     if call.data:
#         mediator.change_parameter(telegram_user_id=call.message.chat.id, parameter=call.data)
#         bot.edit_message_reply_markup(chat_id=call.message.chat.id,
#                                       message_id=call.message.message_id,
#                                       reply_markup=markups.get_parameters_output_inline_markup(
#                                           **mediator.get_parameters_output(telegram_user_id=call.message.chat.id)
#                                       ))
