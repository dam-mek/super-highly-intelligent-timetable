from database.databaseAgent import DBAgent


def get_students():
    database = DBAgent()
    tmp = database.get_students()
    database.close()
    return tmp


def add_student(telegram_user_id: str, name: str):
    database = DBAgent()
    database.add_student(telegram_user_id=telegram_user_id, name=name)
    database.close()


def get_classes():
    database = DBAgent()
    tmp = database.get_classes()
    database.close()
    return tmp


def get_class(number: str, letter: str, subclass: str):
    database = DBAgent()
    tmp = database.get_class(number=number, letter=letter, subclass=subclass)
    database.close()
    return tmp
