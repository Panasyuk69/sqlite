import sqlite3
import time

db = sqlite3.connect('database.db')

db.execute('''CREATE TABLE IF NOT EXISTS students(
           student_id INTEGER PRIMARY KEY AUTOINCREMENT,
           name VARCHAR(50),
           age INTEGER,
           major VARCHAR(50));''')

db.execute('''CREATE TABLE IF NOT EXISTS courses(
           course_id INTEGER PRIMARY KEY AUTOINCREMENT,
           course_name VARCHAR(50),
           instructor VARCHAR(50));''')

db.execute('''CREATE TABLE IF NOT EXISTS student_course(
           student_id INTEGER REFERENCES students (student_id),
           course_id INTEGER REFERENCES courses (course_id),
           PRIMARY KEY (student_id, course_id));''')


def add_user(db, name, age, major):
    db.execute(f'''INSERT INTO students(name, age, major)
               VALUES  (?, ?, ?)''', (name, age, major))
    db.commit()

def add_course(db, course_name, instructor):
    db.execute(f'''INSERT INTO courses(course_name, instructor)
               VALUES  (?, ?)''', (course_name, instructor))
    db.commit()

def get_students(db):
    students = db.execute('''SELECT * FROM students''')
    dict_std = {}
    for student in students:
        dict_std[student[0]] = {'name': student[1], "age": student[2], "major": student[3]}
    db.commit()

    return dict_std

def get_courses(db):
    courses = db.execute('''SELECT * FROM courses''')
    dict_cour = {}
    for course in courses:
        dict_cour[course[0]] = {'course_name': course[1], "instructor": course[2]}
    db.commit()

    return dict_cour

def add_students_to_course(course_id, student_id):
    db.execute(f'''INSERT INTO student_course(course_id, student_id)
               VALUES  (?, ?)''', (course_id, student_id))
    db.commit()

def get_student_course(db, course_id):
    student_course = db.execute(f'''SELECT * FROM students
                                JOIN student_course ON students.id = student_course.student_id
                                WHERE student_course.course_id = ?''', (course_id,))
    return student_course


while True:
    print('1. Добавить нового студента')
    print('2. Добавить новый курс')
    print('3. Показать список студентов')
    print('4. Показать список курсов')
    print('5. Зарегестрировать студента на курс')
    print('6. Показать на каком курсе студент')
    print('7. Выйти')

    choose = input('Выберите необходимую опцию')

    if choose == '1':
        name = input('Введите имя: ')
        age = int(input('Введите возраст: '))
        major = input('Введите дисциплину: ')
        add_user(db, name, age, major)
        print(f"{name} добавлен") 

    elif choose == '2':
        course_name = input('Введите название: ')
        instructor = input('Введите инструктора: ')
        add_course(db, course_name, instructor)
        print(f"{course_name} добавлен")

    elif choose == '3':
        print(get_students(db))

    elif choose == '4':
        print(get_courses(db))

    elif choose == '5':
        course_id = int(input('ID курса'))
        student_id = int(input('ID студента'))
        add_students_to_course(course_id, student_id)

    elif choose == '6':
        get_student_course(db, course_id)

    elif choose == '7':
        break

    else:
        print("Прошу прощения, я вас не понял. Повторите попытку")
        time.sleep(2)
