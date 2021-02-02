from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import datetime
import calendar
import time
from selenium.common.exceptions import NoSuchElementException, ElementNotInteractableException


class Parser:

    def __init__(self):
        url = 'https://gkl-kemerovo.edupage.org/timetable/'
        print('lego 1')
        chrome_options = Options()
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument('--no-sandbox')
        self.session = webdriver.Chrome(options=chrome_options)
        print('lego 2')
        self.session.get(url)
        print('lego 3')

    def close(self):
        self.session.close()

    def get_timetable(self, needed_class, date):
        self.find_needed_class(needed_class)
        print('downloaded find_needed_class')
        # time.sleep(1)
        self.find_needed_week(date)
        columns = self.session.find_elements_by_xpath(
            '//*[@id="skin_PageContent_1"]/div[4]/div[1]/div[2]/div/div/div[2]/div[2]/div/div[2]/div'
        )
        print('columns')
        return self.get_time_and_subjects(columns, date)

    def find_needed_class(self, needed_class):
        while True:
            print('try find')
            try:
                btn = self.session.find_element_by_xpath(
                    '/html/body/div[2]/div/div/div[1]/div/div/div[4]/div/div[1]/span[1]'
                )
                break
            except NoSuchElementException as e:
                print('Нету такого', e)
        while True:
            print('try click')
            try:
                btn.click()
                break
            except ElementNotInteractableException as e:
                btn = self.session.find_element_by_xpath(
                    '/html/body/div[2]/div/div/div[1]/div/div/div[4]/div/div[1]/span[1]'
                )
                print('Не тыркается', e)

        print('find_needed_class 1')
        while True:
            try:
                class_list = self.session.find_elements_by_xpath(
                    '//*[@id="docbody"]/div[5]/div[3]/ul/li'
                )
                if not class_list:
                    class_list = self.session.find_elements_by_xpath(
                        '//*[@id="docbody"]/div[6]/div[3]/ul/li'
                    )
                break
            except NoSuchElementException as e:
                print('class_list 1', e)
            except ElementNotInteractableException as e:
                print('class_list 2', e)
        print('find_needed_class 2')

        print([elem.text for elem in class_list])
        for elem in class_list:
            # print(elem.text, needed_class)
            if elem.text == needed_class:
                elem.click()
                break
        else:
            print('fuck')
            raise Exception('fuck')

    def find_needed_week(self, date):
        tmp_xpath = '//*[@id="skin_PageContent_1"]/div[4]/div[1]/div[2]/div/div/div[2]/div[1]/div/div[2]/div'
        date, day_in_week = self.get_date_and_day_in_week(date)
        dates = []
        print(date, day_in_week)
        for elem in self.session.find_elements_by_xpath(tmp_xpath):
            day = elem.text.split()
            if day:
                dates.append(self.get_date(day[1]))
        print(0, dates)
        while dates[day_in_week] < date:
            next_btn = self.session.find_element_by_xpath('//*[@id="skin_PageContent_1"]/div[4]/div[1]/div[1]/span[6]')
            next_btn.click()
            time.sleep(1)
            dates = []
            for elem in self.session.find_elements_by_xpath(tmp_xpath):
                day = elem.text.split()
                if day:
                    dates.append(self.get_date(day[1]))
            print(1, dates)
        while dates[day_in_week] > date:
            prev_btn = self.session.find_element_by_xpath('//*[@id="skin_PageContent_1"]/div[4]/div[1]/div[1]/span[4]')
            prev_btn.click()
            time.sleep(1)
            dates = []
            for elem in self.session.find_elements_by_xpath(tmp_xpath):
                day = elem.text.split()
                if day:
                    dates.append(self.get_date(day[1]))
            print(2, dates)
        print('week was found')

    def get_time_and_subjects(self, days, date):
        """
        :param days:
        :param date:
        :return: list of raw_subjects
        """
        print('times 1')
        times = self.get_times()
        print('times 2')
        date, day_in_week = self.get_date_and_day_in_week(date)
        raw_subjects = {}
        for block in days[day_in_week * 2].find_elements_by_xpath('./div'):
            size = self.get_size(block)  # it should be get styles
            size_index = (size['top'], size['left'], size['height'], size['width'])
            if block.text:
                if size_index not in raw_subjects:
                    raw_subjects[size_index] = []
                raw_subjects[size_index].append(block.text)
        subjects = []
        print('letsgoooo')
        for position, information_of_lesson in raw_subjects.items():
            for time_key in range(position[0], position[0] + position[2], 52):
                subjects.append(self.get_subject(times[time_key], information_of_lesson))
        return subjects

    def get_times(self):
        times = self.session.find_elements_by_xpath(
            '//*[@id="skin_PageContent_1"]/div[4]/div[1]/div[2]/div/div/div[2]/div[2]/div/div[1]/div'
        )
        times = {self.get_size(elem)['top']: elem.text.split()[1] for elem in times}
        return times

    @staticmethod
    def get_subject(time_of_subject, information_of_lesson):
        if len(information_of_lesson) == 1:
            subject = dict(
                startLesson=time_of_subject.split('-')[0],
                endLesson=time_of_subject.split('-')[1],
                subject=information_of_lesson[0],
            )
        elif len(information_of_lesson) == 2:
            subject = dict(
                startLesson=time_of_subject.split('-')[0],
                endLesson=time_of_subject.split('-')[1],
                teacherName=information_of_lesson[0],
                subject=information_of_lesson[1],
            )
        else:
            subject = dict(
                startLesson=time_of_subject.split('-')[0],
                endLesson=time_of_subject.split('-')[1],
                roomNumber=information_of_lesson[0].split('\n')[-1],
                teacherName=information_of_lesson[1],
                subject=information_of_lesson[2],
            )
        return subject

    @staticmethod
    def get_date_and_day_in_week(date: str):
        print(date)
        date = '-'.join([x.rjust(2, '0') for x in date.split('.')[::-1]])
        print(date)
        date = datetime.date.fromisoformat(date)
        print(date)
        day_in_week = calendar.weekday(year=date.year, month=date.month, day=date.day)
        print(day_in_week)
        return date, day_in_week

    @staticmethod
    def get_date(date: str):
        date = date.split('/')
        date = f'2021-{date[1]}-{date[0]}'
        date = datetime.date.fromisoformat(date)
        return date

    @staticmethod
    def get_size(element):
        size = dict(
            top=-1,
            left=-1,
            height=-1,
            width=-1,
        )
        for selector in element.get_attribute(name='style').split('; '):
            for elem in size:
                if selector.startswith(elem):
                    scale = selector.split()[1]
                    size[elem] = scale[:scale.index('px')]
        if size['top'] == -1 or size['left'] == -1 or size['height'] == -1 or size['width'] == -1:
            raise Exception('Fuck')
        for elem in size:
            size[elem] = round(float(size[elem]) / 52) * 52
        return size
