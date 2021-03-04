import os
import psycopg2
from stuff import Group, Student


def wrapper_database(func):
    # conn = psycopg2.connect(dbname='superhighintelligentdb',
    #                              user='postgres',
    #                              password=os.environ['passwordpsql'],
    #                              host='localhost',
    #                              port='5432')
    def inner(**kwargs):
        if 'cursor' not in kwargs:
            conn = psycopg2.connect(os.environ['DATABASE_URL'], sslmode='require')
            cursor = conn.cursor()
            func(**kwargs, cursor=cursor)
            conn.commit()
            conn.close()
            cursor.close()
        else:
            func(**kwargs)
    return inner


@wrapper_database
def add_student(student: Student, group: Group, cursor=None) -> bool:
    cursor.execute(
        f"""INSERT INTO student (user_id, name, surname) 
            VALUES ('{student.user_id}', '{student.name}', '{student.surname}');"""
    )
    cursor.execute(
        f"""INSERT INTO output_parameters 
        VALUES ({get_student_id(student=student, cursor=cursor)}, DEFAULT, DEFAULT, DEFAULT, DEFAULT, DEFAULT);"""
    )
    success = connect_student_and_class(student=student, group=group, cursor=cursor)
    return success


@wrapper_database
def overwrite_student(new_student: Student, new_group: Group, cursor=None):
    cursor.execute(
        f"""DELETE FROM student 
            WHERE student_id = {get_student_id(student=new_student, cursor=cursor)};"""
    )
    success = add_student(student=new_student, group=new_group, cursor=cursor)
    return success


@wrapper_database
def connect_student_and_class(student_id: int, group: Group, cursor=None) -> bool:
    cursor.execute(
        f"""INSERT INTO student_school_group (student_id, school_group_id) 
            VALUES ('{student_id}', '{get_group_id(group=group, cursor=cursor)}');"""
    )
    return True


@wrapper_database
def change_output_parameters(student_id: int, new_parameters, cursor=None):
    cursor.execute(
        f"""UPDATE output_parameters 
            SET (start_lesson, end_lesson, room_number, teacher_name, subject) = 
            ({new_parameters['start_lesson']}, {new_parameters['end_lesson']}, {new_parameters['room_number']}, 
            {new_parameters['teacher_name']}, {new_parameters['subject']}) 
            WHERE student_id = {student_id};"""
    )
    return True


@wrapper_database
def get_output_parameters(student_id: int, cursor=None):
    cursor.execute(
        f"""SELECT start_lesson, end_lesson, room_number, teacher_name, subject
            FROM output_parameters 
            WHERE student_id = '{student_id}';"""
    )
    raw_parameters = cursor.fetchone()
    parameters = {
        'start_lesson': raw_parameters[0],
        'end_lesson': raw_parameters[1],
        'room_number': raw_parameters[2],
        'teacher_name': raw_parameters[3],
        'subject': raw_parameters[4],
    }
    return parameters


@wrapper_database
def get_group_id(group: Group, cursor=None) -> str:
    """
    Gives group's id in database.

    :param group:
    :param cursor:
    :return:
    """
    cursor.execute(
        f"""SELECT id
            FROM school_group 
            WHERE number = '{group.number}' AND letter = '{group.letter}' AND subclass = '{group.subclass}';"""
    )
    return cursor.fetchone()


@wrapper_database
def get_group(group_id: int, cursor=None) -> Group:
    cursor.execute(
        f"""SELECT number, letter, subclass
            FROM school_group 
            WHERE id = '{group_id}';"""
    )
    number, letter, subclass = cursor.fetchone()
    return Group(number=number, letter=letter, subclass=subclass)


@wrapper_database
def get_student_id(student: Student, cursor=None) -> int:
    """
    Gives student's id in database.

    :param student:
    :param cursor:
    :return:
    """
    cursor.execute(
        f"""SELECT id
            FROM student 
            WHERE user_id = '{student.user_id}' 
    ;"""
    )
    return cursor.fetchone()[0]


@wrapper_database
def get_student(student_id: int, cursor=None) -> Student:
    cursor.execute(
        f"""
        SELECT user_id, name, surname
        FROM student 
        WHERE id = '{student_id}' 
    ;"""
    )
    user_id, name, surname = cursor.fetchone()
    return Student(user_id=user_id, name=name, surname=surname)


@wrapper_database
def get_student_groups(student_id: int, cursor=None):
    """
    Gives a list of groups that the student has chosen.

    :param student_id:
    :param cursor:
    :return:
    """
    cursor.execute(
        f"""
        SELECT school_group_id
        FROM student_school_group 
        WHERE student_id = '{student_id}' 
    ;""")
    list_groups = []
    for group_id in cursor.fetchall():
        list_groups.append(get_group(group_id=group_id, cursor=cursor))
    return list_groups


@wrapper_database
def get_students(cursor=None) -> int:
    cursor.execute("""SELECT * FROM student;""")
    return cursor.fetchall()


@wrapper_database
def get_groups(cursor=None):
    cursor.execute("""SELECT * FROM school_group;""")
    return cursor.fetchall()
