import time
import parserEduPage


def main(number, letter, subclass, date):

    start_time = time.time()
    tt = parserEduPage.Parser()
    print('Время открытия браузера:', time.time() - start_time)
    start_time1 = time.time()
    timetable = tt.get_timetable(f'{number}{letter}-{subclass}'.lower(), date)
    for subject in timetable:
        for information in subject:
            print(information, subject[information], sep=': ')
        print()
    print('Время поиска расписания:', time.time() - start_time1)
    print('Время общее:', time.time() - start_time)
    time.sleep(500)


if __name__ == '__main__':
    puts = open('input.txt', 'r', encoding='utf-8').read().split()
    
    main(puts[0], puts[1], puts[2], puts[3])
