import time
from parserEduPage import parserEduPage


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
