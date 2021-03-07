import datetime
import time
import pytz

timezone = pytz.timezone('Etc/GMT-7')


def get_subclasses(number: str, letter: str):
    number = int(number)
    if letter == 'А':
        return ('АФ', 'РФ') if number % 2 else ('1', '2')
    if letter == 'Б':
        return '1', '2'
    if letter == 'В':
        return 'ХБ', 'ХМ'
    if letter == 'Г':
        return 'ИМО', 'ПР' if number == 11 else 'СЭ'
    if letter == 'Д':
        if number < 10:
            return '1', '2'
        return 'ИТ', 'У' if number == 10 else 'ФТ'


def _subtract_times(time1: datetime.datetime.time, time2: datetime.datetime.time) -> datetime.timedelta:
    tmp_date = datetime.date(1, 1, 1)
    datetime1 = datetime.datetime.combine(tmp_date, time1)
    datetime2 = datetime.datetime.combine(tmp_date, time2)
    return datetime1 - datetime2


def get_remaining_time() -> (int, datetime.timedelta):
    """
    Gives remaining time to end lesson.

    codes:
    0 - ok
    1 - school recess
    2 - today is Sunday
    3 - lessons have ended
    4 - lessons haven't started yet
    5 - я хз (fuck)

    :return: int the cod and time to bell
    """
    now = datetime.datetime.now()

    if now.weekday() == 6 and False:
        return 2, now.time()

    now_time = now.time()
    # now_time = datetime.datetime.strptime('08:46', '%H:%M').time()

    schedule = [
        ('08:00', '08:40'),
        ('08:45', '08:40'),
        ('08:00', '08:40'),
        ('08:00', '08:40'),
        ('08:00', '08:40'),
        ('08:00', '08:40'),
        ('08:45', '09:25'),
        ('09:35', '10:15'),
        ('10:30', '11:10'),
        ('11:25', '12:05'),
        ('12:20', '13:00'),
        ('13:20', '14:00'),
        ('14:05', '14:45'),
        ('14:55', '15:35'),
        ('15:50', '16:30'),
    ]

    schedule = list(map(
        lambda p: (datetime.datetime.strptime(p[0], '%H:%M').time(), datetime.datetime.strptime(p[1], '%H:%M').time()),
        schedule
    ))

    if now_time < schedule[0][0]:
        return 4, now_time

    if now_time >= schedule[-1][1]:
        return 3, now_time

    prev = schedule[-1][0]
    for period in schedule[::-1]:
        if period[0] <= now_time:
            if now_time < period[1]:
                return 0, _subtract_times(period[1], now_time)
            else:
                return 1, _subtract_times(prev, now_time)
        prev = period[0]

    return 5, now_time


def get_text_time(seconds: int) -> str:

    text_time = ''
    minutes, seconds = seconds // 60, seconds % 60
    if minutes:
        form = get_numeral_form(minutes)
        if form == 0:
            ending = 'а'
        elif form == 1:
            ending = 'ы'
        else:
            ending = ''
        text_time += f'{minutes} минут{ending}'

    if minutes and seconds:
        text_time += ' '

    if seconds:
        form = get_numeral_form(seconds)
        if form == 0:
            ending = 'а'
        elif form == 1:
            ending = 'ы'
        else:
            ending = ''
        text_time += f'{seconds} секунд{ending}'
    return text_time


def get_numeral_form(number: int) -> int:
    """
    Gives code od numeral form.

    codes:
    0 - singular (example: 1 минута, 51 секунда)
    1 - dual form (example: 2 минуты, 23 минуты)
    2 - plural (example: 5 минут, 12 секунд)

    :param number:
    :return: int code
    """
    if 11 <= number <= 20:
        return 2
    if number % 10 == 1:
        return 0
    if 2 <= number % 10 <= 4:
        return 1
    return 2


class Group:

    def __init__(self, number, letter, subclass):
        self.number = number
        self.letter = letter
        self.subclass = subclass

    def __str__(self):
        return f'{self.number}{self.letter}-{self.subclass}'.lower()


class Student:

    def __init__(self, user_id, name='no name', surname='', method=None):
        self.method = method
        self.user_id = user_id
        if self.method is not None:
            self.user_id = self.method + '-' + user_id
        self.name = name
        self.surname = surname

    def __str__(self):
        return f'{self.name}'
