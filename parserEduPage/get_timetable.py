import time
from parserEduPage import parserEduPage
import datetime
import pytz
import calendar

timezone = pytz.timezone('Etc/GMT-7')


def get_timetable(needed_class: str, day: str, month: str):
    date = f'{day}.{month}.2021'
    start_time = time.time()
    tt = parserEduPage.Parser()
    print('Время открытия браузера:', time.time() - start_time)
    start_time1 = time.time()
    timetable = tt.get_timetable(needed_class=needed_class, date=date)
    for subject in timetable:
        for information in subject:
            print(information, subject[information], sep=': ')
        print()
    print('Время поиска расписания:', time.time() - start_time1)
    print('Время общее:', time.time() - start_time)
    tt.close()
    return timetable


def get_text_timetable(needed_class, needed_date, output_parameters):
    changing_date = {
        'yesterday': -1,
        'today': 0,
        'tomorrow': 1,
        'after_tomorrow': 2,
    }
    weekend = {
        0: 'Понедельник',
        1: 'Вторник',
        2: 'Среда',
        3: 'Четверг',
        4: 'Пятница',
        5: 'Суббота',
        6: 'Воскресенье',
    }
    subjects = {
        'инф-ка': 'Информатика',
        'мат': 'Математика',
        'р.лит.': 'Родная литература',
        'лит-ра': 'Литература',
        'англ': 'Английский',
        'рос.в мире': 'Россия в мире',
        'физ-ра': 'Физическая культура',
        'фр2': 'Французский',
        'рус яз': 'Русский язык',
        'естест.': 'Естествознание',
        'общ': 'Обществознание',
        'геогр': 'География',
        'техн.': 'Технология',
        'техн': 'Технология',
        'био': 'Биология',
        'физ': 'Физика',
        'хим': 'Химия',
        'астро': 'Астрономия',
        'хпс': 'Химия природных соединений',
        'нем': 'Немецкий',
        'всеоб.ист': 'Всеобщая история',
        'изо': 'Изобразительное искусство',
        'истор': 'История',
        'мхк': 'Мы Хотим Какать',
        'особ.разв.рос ': 'Особености развития российского государства',
    }

    print(needed_class)
    needed_date = datetime.datetime.now(timezone).date() + datetime.timedelta(days=changing_date[needed_date])
    raw_timetable = get_timetable(needed_class=needed_class,
                                  day=str(needed_date.day),
                                  month=str(needed_date.month))
    raw_timetable.sort(key=lambda info: datetime.datetime.strptime(info['start_lesson'], '%H:%M'))

    # очищием расписание от ненужных параметров
    timetable = [dict() for _ in range(len(raw_timetable))]
    for i in range(len(raw_timetable)):
        for key in raw_timetable[i]:
            if output_parameters[key]:
                timetable[i][key] = raw_timetable[i][key]

    # меняем названия предметов на полные
    if output_parameters['subject']:
        for i in range(len(raw_timetable)):
            timetable[i]['subject'] = subjects[timetable[i]['subject'].lower()]

    day_in_week = calendar.weekday(year=2021, month=needed_date.month, day=needed_date.day)

    timetable_text = f"{needed_date.strftime('%d.%m.%y')} {weekend[day_in_week]} {str(needed_class).upper()}\n\n"
    for subject in timetable:
        if 'start_lesson' in subject:
            timetable_text += f"{subject['start_lesson']}"
            if 'end_lesson' in subject:
                timetable_text += f"-"
        if 'end_lesson' in subject:
            timetable_text += f"{subject['end_lesson']}"
        if 'end_lesson' in subject or 'start_lesson' in subject:
            timetable_text += f": "
        if 'subject' in subject:
            timetable_text += f"{subject['subject']} "
        if 'teacher_name' in subject:
            timetable_text += f"{subject['teacher_name']} "
        if 'room_number' in subject:
            timetable_text += f"(каб. {subject['room_number']})"
        timetable_text += '\n'

    return timetable_text
