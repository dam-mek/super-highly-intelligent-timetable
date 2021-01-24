import os
import psycopg2


class DBAgent:

    def __init__(self):
        self.conn = psycopg2.connect(dbname='superhighintelligentdb',
                                     user='postgres',
                                     password=os.environ['passwordpsql'],
                                     host='localhost',
                                     port='5432')
        self.cursor = self.conn.cursor()

    def add_student(self, telegram_user_id, name) -> None:
        self.cursor.execute(
            f"""INSERT INTO student (telegram_user_id, name) VALUES ('{telegram_user_id}', '{name}');"""
        )
        self.conn.commit()

    def connect_student_and_class(self, student_id, class_id) -> None:
        self.cursor.execute(f"""
        SELECT id 
        FROM class 
        WHERE number = '{number}' AND letter = '{letter}' AND subclass = '{subclass}' 
        ;""")
        self.conn.commit()

    def get_students(self) -> int:
        self.cursor.execute("""SELECT * FROM student;""")
        return self.cursor.fetchall()

    def get_classes(self):
        self.cursor.execute("""SELECT * FROM class;""")
        return self.cursor.fetchall()

    def get_class(self, number, letter: int, subclass):
        self.cursor.execute(f"""
        SELECT id 
        FROM class 
        WHERE number = '{number}' AND letter = '{letter}' AND subclass = '{subclass}' 
        ;""")
        return self.cursor.fetchone()

    def close(self):
        self.conn.close()
        self.cursor.close()
