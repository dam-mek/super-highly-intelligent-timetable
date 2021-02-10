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

    def add_student(self, student: Student, group: Group) -> bool:
        self.cursor.execute(
            f"""INSERT INTO student (messenger_user_id, name, surname) 
                VALUES ('{student.messenger_user_id}', '{student.name}', '{student.surname}');"""
        )
        self.cursor.execute(
            f"""INSERT INTO output_parameters 
            VALUES ({self.get_student_id(student)}, DEFAULT, DEFAULT, DEFAULT, DEFAULT, DEFAULT);"""
        )
        success = self.connect_student_and_class(student=student, group=group)
        self.conn.commit()
        return success
    
    def overwrite_student(self, new_student: Student, new_group: Group):
        self.cursor.execute(
            f"""DELETE FROM student 
                WHERE student_id = {self.get_student_id(new_student)};"""
        )
        success = self.add_student(student=new_student, group=new_group)
        return success
    
    def connect_student_and_class(self, student: Student, group: Group) -> bool:
        student_id = self.get_student_id(student)
        group_id = self.get_group_id(group)
        self.cursor.execute(
            f"""INSERT INTO student_school_group (student_id, school_group_id) 
                VALUES ('{student_id}', '{group_id}');"""
        )
        self.conn.commit()
        return True

    def change_output_parameters(self, student: Student, new_parameters):
        self.cursor.execute(
            f"""UPDATE output_parameters 
                SET (start_lesson, end_lesson, room_number, teacher_name, subject) = 
                ({new_parameters['start_lesson']}, {new_parameters['end_lesson']}, {new_parameters['room_number']}, 
                {new_parameters['teacher_name']}, {new_parameters['subject']}) 
                WHERE student_id = {self.get_student_id(student)};"""
        )
        return True

    def get_group_id(self, group: Group) -> str:
        self.cursor.execute(
            f"""SELECT id
                FROM school_group 
                WHERE number = '{group.number}' AND letter = '{group.letter}' AND subclass = '{group.subclass}';"""
        )
        return self.cursor.fetchone()

    def get_group(self, group_id: int) -> Group:
        self.cursor.execute(
            f"""SELECT number, letter, subclass
                FROM school_group 
                WHERE id = '{group_id}';"""
        )
        number, letter, subclass = self.cursor.fetchone()
        return Group(number=number, letter=letter, subclass=subclass)

    def NOT_WORK_get_student_id(self, student: Student) -> int:
        self.cursor.execute(
            f"""SELECT id
                FROM student 
                WHERE messenger_user_id = '{student.messenger_user_id}' 
        ;""")
        return self.cursor.fetchone()

    def NOT_WORK_get_student(self, student_id: int) -> Student:
        self.cursor.execute(
            f"""
            SELECT messenger_user_id, name, surname
            FROM student 
            WHERE id = '{student_id}' 
        ;""")
        messenger_user_id, name, surname = self.cursor.fetchone()
        return Student(messenger_user_id=messenger_user_id, name=name, surname=surname)

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
