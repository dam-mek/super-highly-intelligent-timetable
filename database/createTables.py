import os
import psycopg2
from stuff import get_subclasses


def create_classes(cursor):
    """ create classes in the table class"""

    class_numbers = ['8', '9', '10', '11']
    class_letters = ['А', 'Б', 'В', 'Г', 'Д']
    commands = []
    for number in class_numbers:
        for letter in class_letters:
            for subclass in get_subclasses(number, letter):
                commands.append(
                    f"""INSERT INTO school_group (number, letter, subclass) VALUES ('{number}', '{letter}', '{subclass}');"""
                )
    try:
        for command in commands:
            cursor.execute(command)
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)


def create_tables():
    """ create tables in the PostgreSQL database"""
    commands = (
        """
        DROP SCHEMA public CASCADE;
        CREATE SCHEMA public;""",
        """
        CREATE TABLE student (
            id SERIAL PRIMARY KEY,
            messenger_user_id VARCHAR(128),
            name VARCHAR(64),
            surname VARCHAR(64)
        );""",
        """ 
        CREATE TABLE school_group (
            id SERIAL PRIMARY KEY,
            number VARCHAR(2),
            letter VARCHAR(1),
            subclass VARCHAR(3)
        );""",
        """
        CREATE TABLE student_school_group (
            school_group_id INTEGER REFERENCES school_group(id),
            student_id INTEGER REFERENCES student(id)
        );""",
        """
        CREATE TABLE output_parameters (
            student_id INTEGER REFERENCES student(id),
            start_lesson BOOLEAN DEFAULT TRUE,
            end_lesson BOOLEAN DEFAULT TRUE,
            room_number BOOLEAN DEFAULT TRUE,
            teacher_name BOOLEAN DEFAULT TRUE,
            subject BOOLEAN DEFAULT TRUE
        );""",
    )
    conn = None
    try:
        # connect to the PostgreSQL server
        conn = psycopg2.connect(dbname='superhighintelligentdb',
                                user='postgres',
                                password=os.environ['passwordpsql'],
                                host='localhost',
                                port='5432')
        cursor = conn.cursor()
        # create table one by one
        for command in commands:
            cursor.execute(command)
        create_classes(cursor)

        cursor.close()
        conn.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()


if __name__ == '__main__':
    create_tables()
