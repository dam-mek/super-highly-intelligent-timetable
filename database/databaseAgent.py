import random

class DBAgent:

    def __init__(self):
        pass

    def add_student(self, **information_about_student) -> None:
        pass

    def connect_student_and_class(self, student_id, class_id) -> None:
        pass

    def get_students(self) -> int:
        pass

    def get_classes(self):
        pass

    def get_class(self, number: str, letter: str, subclass: str):
        pass

    def get_parameters_output(self, telegram_user_id: str):
        parameters_output = {
            'start_lesson': bool(random.randint(0, 1)),
            'end_lesson': bool(random.randint(0, 1)),
            'room_number': bool(random.randint(0, 1)),
            'teacher_name': bool(random.randint(0, 1)),
            'subject': bool(random.randint(0, 1))
        }
        return parameters_output

    def change_parameter(self, telegram_user_id: str, parameter: str):
        pass

    def close(self):
        pass
