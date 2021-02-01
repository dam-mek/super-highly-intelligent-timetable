from selenium import webdriver
import datetime
import calendar
import time
from selenium.common.exceptions import NoSuchElementException, ElementNotInteractableException


class Parser:

    def __init__(self):
        url = 'https://gkl-kemerovo.edupage.org/timetable/'
        self.session = webdriver.Chrome()
        self.session.get(url)

    def get_timetable(self, needed_class, date):
        while True:
            try:
                self.find_needed_class(needed_class)
                break
            except NoSuchElementException:
                pass
            except ElementNotInteractableException:
                pass
        # time.sleep(1)
        self.find_needed_week(date)
        columns = self.session.find_elements_by_xpath(
            '//*[@id="skin_PageContent_1"]/div[4]/div[1]/div[2]/div/div/div[2]/div[2]/div/div[2]/div'
        )

        return self.get_time_and_subjects(columns, date)

        # session.close()

    def find_needed_class(self, needed_class):
        btn = self.session.find_element_by_xpath('/html/body/div[2]/div/div/div[1]/div/div/div[4]/div/div[1]/span[1]')
        btn.click()
        class_list = self.session.find_elements_by_xpath('//*[@id="docbody"]/div[6]/div[3]/ul/li')
        sorted_class_list = sorted(class_list, key=lambda x: x.text)
        for elem in sorted_class_list:
            if elem.text == needed_class:
                elem.click()
                break
        else:
            raise Exception('fuck')

    def find_needed_week(self, date):
        tmp_xpath = '//*[@id="skin_PageContent_1"]/div[4]/div[1]/div[2]/div/div/div[2]/div[1]/div/div[2]/div'
        date, day_in_week = self.get_date_and_day_in_week(date)
        dates = []
        for elem in self.session.find_elements_by_xpath(tmp_xpath):
            day = elem.text.split()
            if day:
                dates.append(self.get_date(day[1]))
        while dates[day_in_week] < date:
            next_btn = self.session.find_element_by_xpath('//*[@id="skin_PageContent_1"]/div[4]/div[1]/div[1]/span[6]')
            next_btn.click()
            time.sleep(1)
            dates = []
            for elem in self.session.find_elements_by_xpath(tmp_xpath):
                day = elem.text.split()
                if day:
                    dates.append(self.get_date(day[1]))

        while dates[day_in_week] > date:
            prev_btn = self.session.find_element_by_xpath('//*[@id="skin_PageContent_1"]/div[4]/div[1]/div[1]/span[4]')
            prev_btn.click()
            time.sleep(1)
            dates = []
            for elem in self.session.find_elements_by_xpath(tmp_xpath):
                day = elem.text.split()
                if day:
                    dates.append(self.get_date(day[1]))

    def get_time_and_subjects(self, days, date):
        """


        :param days:
        :param date:
        :return: list of raw_subjects
        """
        times = self.get_times()
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
        print(times)
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
        date = '-'.join(date.split('.')[::-1])
        date = datetime.date.fromisoformat(date)
        day_in_week = calendar.weekday(year=date.year, month=date.month, day=date.day)
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
