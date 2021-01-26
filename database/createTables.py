import os
import psycopg2


def get_subclasses(number, letter):
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


def create_classes(cursor):
    """ create classes in the table class"""

    class_numbers = {8, 9, 10, 11}
    class_letters = {'А', 'Б', 'В', 'Г', 'Д'}
    commands = []
    for number in class_numbers:
        for letter in class_letters:
            for subclass in get_subclasses(number, letter):
                commands.append(
                    f"""
                    INSERT INTO class (number, letter, subclass) VALUES ('{number}', '{letter}', '{subclass}');
                    """
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
        DROP TABLE student CASCADE;
        CREATE TABLE student (
            id SERIAL PRIMARY KEY,
            telegram_user_id VARCHAR(100),
            name VARCHAR(255)
        );""",
        """ 
        DROP TABLE class CASCADE;
        CREATE TABLE class (
            id SERIAL PRIMARY KEY,
            number SMALLINT,
            letter VARCHAR(1),
            subclass VARCHAR(3)
        );""",
        """
        DROP TABLE student_class;
        CREATE TABLE student_class (
            class_id INTEGER REFERENCES class(id),
            student_id INTEGER REFERENCES student(id)
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
