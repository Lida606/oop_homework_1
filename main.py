import random


class Student:
    def __init__(self, name, surname, gender):
        self.name = name
        self.surname = surname
        self.gender = gender
        self.finished_courses = []
        self.courses_in_progress = []
        self.grades = {}

    def add_courses(self, course_name):
        self.finished_courses.append(course_name)

    def average(self):
        grades = []
        summa = 0
        length = 0
        for course in self.grades:
            grades.append(self.grades[course])
        for i in range(len(grades)):
            summa += sum(grades[i])
            length += len(grades[i])
        grade = summa/length
        return grade

    def rate_lec(self, lecturer, course, grade):
        if isinstance(lecturer, Lecturer) and course in lecturer.courses_attached and course in self.courses_in_progress:
            if course in lecturer.grades:
                lecturer.grades[course] += [grade]
            else:
                lecturer.grades[course] = [grade]
        else:
            return 'Ошибка'

    def __str__(self):
        return (f"Имя: {self.name}\nФамилия: {self.surname}\n"
                f"Средняя оценка за домашние задания: {self.average():0.1f}\n"
                f"Курсы в процессе изучения: {', '.join(self.courses_in_progress)}\n"
                f"Завершенные курсы: {', '.join(self.finished_courses)}\n")

    def __lt__(self, other):
        return self.average() < other.average()

    def average_course_lec(self, lecturers, course):
        summa = 0
        length = 0
        grades = []
        for lecturer in lecturers:
            if isinstance(lecturer, Lecturer) and course in lecturer.courses_attached and course in self.courses_in_progress:
                if course in lecturer.grades:
                    grades.append(lecturer.grades[course])
                    for i in range(len(grades)):
                        summa += sum(grades[i])
                        length += len(grades[i])
            else:
                return 'Ошибка'
        return f'Средняя оценка среди лекторов курса {course}: {summa / length:0.2f}'

class Mentor:
    def __init__(self, name, surname):
        self.name = name
        self.surname = surname
        self.courses_attached = []

    def average_course_st(self, students, course):
        summa = 0
        length = 0
        grades = []
        for student in students:
            if isinstance(student, Student) and course in self.courses_attached and course in student.courses_in_progress:
                if course in student.grades:
                    grades.append(student.grades[course])
                    for i in range(len(grades)):
                        summa += sum(grades[i])
                        length += len(grades[i])
            else:
                return 'Ошибка'
        return f'Средняя оценка среди студентов курса {course}: {summa/length:0.2f}'


class Lecturer(Mentor):
    def __init__(self, name, surname):
        super().__init__(name, surname)
        self.grades = {}

    def average(self):
        grades = []
        summa = 0
        length = 0
        for course in self.grades:
            grades.append(self.grades[course])
        for i in range(len(grades)):
            summa += sum(grades[i])
            length += len(grades[i])
        grade = summa/length
        return grade

    def __str__(self):
        return (f"Имя: {self.name}\nФамилия: {self.surname}\n"
                f"Средняя оценка за лекции: {self.average():0.1f}\n")

    def __lt__(self, other):
        return self.average() < other.average()


class Reviewer(Mentor):
    def rate_hw(self, student, course, grade):
        if isinstance(student, Student) and course in self.courses_attached and course in student.courses_in_progress:
            if course in student.grades:
                student.grades[course] += [grade]
            else:
                student.grades[course] = [grade]
        else:
            return 'Ошибка'

    def __str__(self):
        return f"Имя: {self.name}\nФамилия: {self.surname}\n"


student1 = Student('Ruoy', 'Eman', 'your_gender')
student2 = Student('Moly', 'Holy', 'your_gender')
student1.courses_in_progress += ['Python', 'Git', 'SQL']
student2.courses_in_progress += ['Python', 'Git', 'HTML']
student1.add_courses('Введение в программирование')
student2.add_courses('SQL')

reviewer1 = Reviewer('Some', 'Buddy')
reviewer2 = Reviewer('Any', 'One')
reviewer1.courses_attached += ['Python']
reviewer2.courses_attached += ['Git']

lecturer1 = Lecturer('Some', 'Buddy')
lecturer2 = Lecturer('Any', 'One')
lecturer3 = Lecturer('Who', 'Doctor')
lecturer1.courses_attached += ["Python"]
lecturer2.courses_attached += ["Git"]
lecturer3.courses_attached += ["Python"]

for i in range(3):
    student1.rate_lec(lecturer1, "Python", 10 - random.randint(0, 3))
    student1.rate_lec(lecturer2, "Git", 10 - random.randint(0, 3))
    student1.rate_lec(lecturer3, "Python", 10 - random.randint(0, 3))
    student2.rate_lec(lecturer1, "Python", 10 - random.randint(0, 3))
    student2.rate_lec(lecturer2, "Git", 10 - random.randint(0, 3))
    student2.rate_lec(lecturer3, "Python", 10 - random.randint(0, 3))
    reviewer1.rate_hw(student1, 'Python', 10 - random.randint(0, 3))
    reviewer1.rate_hw(student2, 'Python', 10 - random.randint(0, 3))
    reviewer2.rate_hw(student1, 'Git', 10 - random.randint(0, 3))
    reviewer2.rate_hw(student2, 'Git', 10 - random.randint(0, 3))

print(reviewer1, reviewer2, lecturer1, lecturer2, sep="\n")
print(lecturer1 < lecturer2, student1 < student2, end='\n\n')
print(student1, student2, sep='\n')
print(reviewer1.average_course_st([student1, student2], 'Python'))
print(student2.average_course_lec([lecturer1, lecturer3], 'Python'))
