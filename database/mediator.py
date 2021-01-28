from database.databaseAgent import DBAgent


def add_student(**information_about_student):
    database = DBAgent()
    database.add_student(**information_about_student)
    database.close()


def change_parameter(telegram_user_id: str, parameter: str):
    database = DBAgent()
    database.change_parameter(telegram_user_id, parameter)
    database.close()


def get_students():
    database = DBAgent()
    tmp = database.get_students()
    database.close()
    return tmp


def get_parameters_output(telegram_user_id: str):
    database = DBAgent()
    tmp = database.get_parameters_output(telegram_user_id=telegram_user_id)
    database.close()
    return tmp


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
