from datebaseAgent import DBAgent


def main():
    database = DBAgent()
    # database.add_student(123, 'Vasia')
    print(database.get_students())
    print(database.get_classes())
    print(database.get_class(10, 'Д', 'ИТ'))
    database.close()


if __name__ == '__main__':
    main()
