import os
import psycopg2
from stuff import Group, Student


class DBAgent:

    def __init__(self):
        self.conn = psycopg2.connect(dbname='superhighintelligentdb',
                                     user='postgres',
                                     password=os.environ['passwordpsql'],
                                     host='localhost',
                                     port='5432')
        self.cursor = self.conn.cursor()

    def add_student(self, telegram_user_id: str, name: str, surname: str, group: Group) -> bool:
        self.cursor.execute(
            f"""INSERT INTO student (telegram_user_id, name, surname) VALUES ('{telegram_user_id}', '{name}', '{surname}'); """
        )
        student = Student(telegram_user_id, name, surname)
        success = self.connect_student_and_class(student=student, group=group)
        self.conn.commit()
        return success
    
    def overwrite(self, telegram_user_id: str, new_name: str, new_surname: str, new_group: Group):
        pass
    
    def connect_student_and_class(self, student: Student, group: Group) -> bool:
        student_id = self.get_student_id(student)
        group_id = self.get_group_id(group)
        self.cursor.execute(
            f"""INSERT INTO student_school_group (student_id, school_group_id) VALUES ('{student_id}', '{group_id}');"""
        )
        self.conn.commit()
        return True

    def change_output_parameters(self, student: Student, new_parameters):
        pass

    def get_group_id(self, group: Group) -> str:
        self.cursor.execute(
            f"""
            SELECT id
            FROM school_group 
            WHERE number = '{group.number}' AND letter = '{group.letter}' AND subclass = '{group.subclass}' 
        ;""")
        return self.cursor.fetchone()

    def get_group(self, group_id: str) -> Group:
        self.cursor.execute(
            f"""
            SELECT number, letter, subclass
            FROM school_group 
            WHERE id = '{group_id}' 
        ;""")
        number, letter, subclass = self.cursor.fetchone()
        return Group(number=number, letter=letter, subclass=subclass)

    def get_student_id(self, student: Student) -> str:
        self.cursor.execute(
            f"""
            SELECT id
            FROM student 
            WHERE telegram_user_id = '{student.telegram_user_id}' 
        ;""")
        return self.cursor.fetchone()

    def get_student(self, student_id: str) -> Student:
        self.cursor.execute(
            f"""
            SELECT telegram_user_id, name, surname
            FROM student 
            WHERE id = '{student_id}' 
        ;""")
        telegram_user_id, name, surname = self.cursor.fetchone()
        return Student(telegram_user_id=telegram_user_id, name=name, surname=surname)

    def get_student_groups(self, student: Student):
        pass

    def get_output_parameters(self, student: Student):
        pass

    def get_students(self) -> int:
        self.cursor.execute("""SELECT * FROM student;""")
        return self.cursor.fetchall()

    def get_classes(self):
        self.cursor.execute("""SELECT * FROM class;""")
        return self.cursor.fetchall()

    def get_class(self, number: str, letter: str, subclass: str):
        self.cursor.execute(f"""
        SELECT id 
        FROM class 
        WHERE number = '{number}' AND letter = '{letter}' AND subclass = '{subclass}' 
        ;""")
        return self.cursor.fetchone()

    def close(self):
        self.conn.close()
        self.cursor.close()
