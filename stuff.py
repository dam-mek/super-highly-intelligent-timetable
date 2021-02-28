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


class Group:

    def __init__(self, number, letter, subclass):
        self.number = number
        self.letter = letter
        self.subclass = subclass

    def __str__(self):
        return f'{self.number}{self.letter}-{self.subclass}'.lower()
