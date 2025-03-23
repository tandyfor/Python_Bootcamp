import random
import time
import multiprocessing.dummy as multiprocessing
import threading

import prettytable
import curses

BAD = 0
NEUTRAL = 1
GOOD = 2

MOOD = [BAD, NEUTRAL, GOOD]
MOOD_WEIGHTS = [0.125, 0.625, 0.25]

MALE = "М"
FEMALE = "Ж"

IN_LINE = "Очередь"
SUCCESS = "Сдал"
FAIL = "Провалил"

class Person():
    def __init__(self, name, gender) -> None:
        self.name = name
        self.gender = gender
        self.status = None

    def __str__(self) -> str:
        return f"{self.name}"


class Student(Person):
    def __init__(self, name, gender):
        super().__init__(name, gender)
        self.status = IN_LINE
        self.exam_time = 0

    def get_row(self):
        return self.name, self.status
    
    
class Examiner(Person):
    def __init__(self, name, gender):
        super().__init__(name, gender)
        self.status = "Свободен"
        self.start_time = time.time()
        self.work_time = 0
        self.take_dinner = False
        self.students_count = 0
        self.flunked_student = 0
    
    def get_work_time(self):
        return self.work_time
    
    def update_work_time(self):
        self.work_time = time.time() - self.start_time

    def get_row(self):
        time = f"{self.get_work_time():.2f}"
        return self.name, self.status, self.students_count, self.flunked_student, time

    def dinner(self):
        if not self.take_dinner and self.get_work_time() > 30:
            self.status = '-'
            self.take_dinner = True
            time.sleep(random.randint(12, 18))


class Question():
    def __init__(self, question):
        self.question = question
        self.success_count = 0

    def __str__(self) -> str:
        return self.question.rstrip()

    def get_question(self):
        return self.question


class Exam():
    def __init__(self, examiner: Examiner, student: Student, questions: list[Question]) -> None:
        self.examiner = examiner
        self.student = student
        self.questions = random.choices(questions, k=3)
        self.mood = random.choices(MOOD, MOOD_WEIGHTS, k=1)[0]

    def exam(self):
        self.examiner.status = self.student.name
        exam_time = len(self.examiner.name) + random.randint(-1, 1) 
        time.sleep(exam_time)
        self.student.exam_time = exam_time
        self.examiner.students_count += 1
        grade = self.ask_questions()
        if self.mood == BAD:
            self.student.status = FAIL
        elif self.mood == GOOD:
            self.student.status = SUCCESS
        else:
            self.student.status = SUCCESS if grade else FAIL
        if self.student.status == FAIL:
            self.examiner.flunked_student += 1
        self.examiner.update_work_time()

    def get_weights(self, len: int, gender: str):
        sequence = [1/2, 1/3]
        current = 3
        for _ in range(2, len):
            current *= 2
            sequence.append(1 / current)
        return sequence[0:len] if gender == MALE else list(reversed(sequence))[0:len]
    
    def ask_questions(self):
        results = []
        for question in self.questions:
            true_answers = []
            student_answers = [] 
            student_answers.append(self.get_answer(question.get_question()))
            while random.random() < 1 / 3:
                student_answer = self.get_answer(question.get_question())
                if student_answer not in student_answers:
                    student_answers.append(student_answer)

            true_answers.append(self.check_answer(question.get_question()))
            while random.random() < 1 / 3:
                true_answer = self.check_answer(question.get_question())
                if true_answer not in true_answers:
                    true_answers.append(true_answer)
            
            grade = self.get_grade(student_answers, true_answers)
            results.append(grade)
            if grade:
                question.success_count += 1
        return True if results.count(True) > 1 else False

    def get_answer(self, question: list[str]):
        return random.choices(question, self.get_weights(len(question), self.student.gender), k=1)[0]

    def check_answer(self, question: list[str]):
        return random.choices(question, self.get_weights(len(question), self.examiner.gender), k=1)[0]

    def get_grade(self, student_answers: list[str], true_answers: list[str]):
        true_count = 0
        false_count = 0
        for answer in student_answers:
            if answer in true_answers:
                true_count += 1
            else:
                false_count += 1
        return True if (true_count - false_count) / len(true_answers) > 0.5 else False

class Viewer():
    def __init__(self) -> None:
        self.students_tabel = prettytable.PrettyTable()
        self.students_tabel.field_names = ["Студент", "Статус"]
        
        self.examiner_tabel = prettytable.PrettyTable()
        self.examiner_tabel.field_names = ["Экзаменатор", "Текущий студент", "Всего студентов", "Завалил", "Время работы"]

        self.students: list[Student]
        self.examiners: list[Examiner]

        self.status_dict = {IN_LINE : 0, SUCCESS : 1, FAIL : 2}

    def update_student(self):
        self.students_tabel.clear_rows()
        self.students.sort(key=lambda x: self.status_dict.get(x.status))
        for student in self.students:
            self.students_tabel.add_row(student.get_row())

    def update_examiner(self):
        self.examiner_tabel.clear_rows()
        for examiner in self.examiners:
            self.examiner_tabel.add_row(examiner.get_row())

    def __str__(self):
        return f"{self.students_tabel}\n{self.examiner_tabel}"
        

def worker(examiner: Examiner, students: list[Student], questions: list[str]):
    while not students.empty():
        start = time.time()
        student = students.get()
        exam = Exam(examiner, student, questions)
        exam.exam()
        delta = time.time() - start
        print(examiner, student, f" exam time: {delta:.2f} all work time: {examiner.get_work_time():.2f}")
        examiner.dinner()
        
def printer(examiners: multiprocessing.Queue, students_list: list[Student], examers: list[Examiner]):
    stdscr = curses.initscr()
    curses.noecho()
    curses.cbreak()
    stdscr.keypad(True)
    curses.curs_set(0)
    time.sleep(0.1)
    height, width = stdscr.getmaxyx()
    
    v = Viewer()
    v.students = students_list
    v.examiners = examers
    s = time.time()

    while not len(threading.enumerate()) == 2:
        v.update_examiner()
        v.update_student()
        stdscr.clear()
        add_s_1 = f"\nОсталось в очереди {len(list(filter(lambda x: x.status == 'Очередь', students_list)))} из {len(students_list)}"
        add_s_2 = f"\nВремя с начала экзамена: {time.time() - s:.2f}"
        stdscr.addstr(0, 0, str(v) + add_s_1 + add_s_2)
        stdscr.refresh()
        stdscr.refresh()
        time.sleep(0.1)
    
    curses.nocbreak(); stdscr.keypad(False); curses.echo()
    curses.endwin()


def read_file(filename: str):
    with open(filename, "r") as file:
        return file.readlines()
    
def print_top(values_list, output_str):
    if values_list:
        print(output_str, end="")
        for i, value in enumerate(values_list):
            print(value, end=", " if i != 2 else "")
            if i == 2:
                break
        print()

def end_print(students_list, examers, questions, s):
    v = Viewer()
    v.students = students_list
    v.examiners = examers
    v.update_examiner()
    v.update_student()
    v.examiner_tabel.del_column("Текущий студент")
    print("\033c")
    print(v)
    print(f"Время с момента начала экзамена и до момента и его завершения: {time.time() - s:.2f}")

    success_students = list(filter(lambda x: x.status == SUCCESS, students_list))
    success_students.sort(key=lambda x: x.exam_time)
    print_top(success_students, "Имена лучших студентов: ")
    
    examers = list(filter(lambda x: x.students_count != 0, examers))
    examers.sort(key=lambda x: x.flunked_student / x.students_count)
    print_top(examers, "Имена лучших экзаменаторов: ")
    fail_students = list(filter(lambda x: x.status == FAIL, students_list))
    fail_students.sort(key=lambda x: x.exam_time)
    print_top(fail_students, "Имена студентов, которых после экзамена отчислят: ")
    questions.sort(key=lambda x: x.success_count)
    print_top(questions, "Лучшие вопросы: ")
    print(f"Вывод: {"экзамен удался" if len(success_students) / len(students_list) > 0.85 else "экзамен не удался"}")

def main():
    students = multiprocessing.Queue()
    examiners = multiprocessing.Queue()
    
    students_list = list(map(lambda line: Student(line.split()[0], line.split()[1]), read_file("students.txt")))
    examers = list(map(lambda line: Examiner(line.split()[0], line.split()[1]), read_file("examiners.txt")))
    questions = list(map(Question, read_file("questions.txt")))

    for student in students_list:
        students.put(student)

    processes = []
    
    printer_thread = multiprocessing.Process(target=printer, args=(examiners, students_list, examers))
    printer_thread.start()

    for examiner in examers:
        p = multiprocessing.Process(target=worker, args=(examiner, students, questions))
        processes.append(p)
        p.start()

    s = time.time()

    for p in processes:
        p.join()

    printer_thread.join()
    end_print(students_list, examers, questions, s)


if __name__ == "__main__":
    main()