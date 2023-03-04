from pprint import pprint

from sqlalchemy import func, desc, select, and_

from src.models import Teacher, Student, Discipline, Grade, Group
from src.db import session


def select_1():
    """Найти 5 студентов с наибольшим средним баллом по всем предметам."""
    result = session.query(Student.fullname, func.round(func.avg(Grade.grade), 2).label('avg_grade')) \
        .select_from(Grade).join(Student).group_by(Student.id).order_by(desc('avg_grade')).limit(5).all()
    return result

def select_2(discipline_id):
    """Найти студента с наивысшим средним баллом по определенному предмету.
    """
    r = session.query(Discipline.name,
                      Student.fullname,
                      func.round(func.avg(Grade.grade), 2).label('avg_grade')
                      ) \
        .select_from(Grade) \
        .join(Student) \
        .join(Discipline) \
        .filter(Discipline.id == discipline_id) \
        .group_by(Student.id, Discipline.name) \
        .order_by(desc('avg_grade')) \
        .limit(1).all()
    return r

def select_3(discipline_id):
    """Найти средний балл в группах по определенному предмету.
    """
    r = session.query(Discipline.name,
                      Group.name,
                      func.round(func.avg(Grade.grade), 2).label('avg_grade')
                      ) \
        .select_from(Grade) \
        .join(Student) \
        .join(Group) \
        .join(Discipline) \
        .filter(Discipline.id == discipline_id) \
        .group_by(Group.id, Discipline.name) \
        .order_by(Group.id) \
        .all()
    return r

def select_4():
    """Найти средний балл на потоке (по всей таблице оценок).
    """
    r = session.query(func.round(func.avg(Grade.grade), 2).label('average_grade')).select_from(Grade).all()
    return r

def select_5():
    """Найти какие курсы читает определенный преподаватель.
    """
    r = session.query(Teacher.fullname,
                      Discipline.name,
                      ) \
        .select_from(Discipline) \
        .join(Teacher) \
        .order_by(Teacher.fullname) \
        .all()
    return r

def select_6(group_id):
    """Найти список студентов в определенной группе.
    """
    r = session.query(Group.name,
                      Student.fullname,
                      ) \
        .select_from(Student) \
        .join(Group) \
        .filter(Group.id == group_id) \
        .order_by(Student.fullname) \
        .all()
    return r

def select_7(group_id, discipline_id):
    """Найти оценки студентов в отдельной группе по определенному предмету.
    """
    r = session.query(Student.fullname,
                      Group.name,
                      Discipline.name,
                      Grade.grade,
                      Grade.date_of
                      ) \
        .select_from(Grade) \
        .join(Student) \
        .join(Discipline) \
        .join(Group) \
        .filter(and_(Group.id == group_id), (Discipline.id == discipline_id)) \
        .order_by(Student.fullname) \
        .all()
    return r

def select_8(teacher_id):
    """Найти средний балл, который ставит определенный преподаватель по своим предметам.
    """
    r = session.query(Teacher.fullname,
                      Discipline.name,
                      func.round(func.avg(Grade.grade), 2).label('avg_grade')
                      ) \
        .select_from(Grade) \
        .join(Discipline) \
        .join(Teacher) \
        .filter(Teacher.id == teacher_id) \
        .group_by(Discipline.name, Teacher.fullname) \
        .all()
    return r

def select_9(student_id):
    """Найти список курсов, которые посещает определенный студент."""
    r = session.query(Student.fullname,
                      Discipline.name,
                      Grade.date_of
                      ) \
        .select_from(Grade) \
        .join(Student) \
        .join(Discipline) \
        .filter(Student.id == student_id) \
        .order_by(Discipline.name) \
        .all()
    return r

def select_10(student_id, teacher_id):
    """Список курсов, которые определенному студенту читает определенный преподаватель."""
    r = session.query(Discipline.name,
                      Student.fullname,
                      Teacher.fullname,
                      Grade.date_of
                      ) \
        .select_from(Grade) \
        .join(Student) \
        .join(Discipline) \
        .join(Teacher) \
        .filter(and_(Student.id == student_id), (Teacher.id == teacher_id)) \
        .order_by(Discipline.name) \
        .all()
    return r

def select_11(student_id, teacher_id):
    """    Средний балл, который определенный преподаватель ставит определенному студенту.
    """
    r = session.query(Teacher.fullname,
                      Student.fullname,
                      Discipline.name,
                      func.round(func.avg(Grade.grade), 2).label('avg_grade')
                      ) \
        .select_from(Grade) \
        .join(Student) \
        .join(Discipline) \
        .join(Teacher) \
        .filter(and_(Student.id == student_id), (Teacher.id == teacher_id)) \
        .group_by(Discipline.name, Teacher.fullname, Student.fullname) \
        .all()
    return r

def select_12(discipline_id, group_id):
    """Оценки студентов в определенной группе по определенному предмету на последнем занятии."""
    subquery = (select(Grade.date_of).join(Student).join(Group).where(
        and_(Grade.discipline_id == discipline_id, Group.id == group_id)
    ).order_by(desc(Grade.date_of)).limit(1).scalar_subquery())

    r = session.query(Discipline.name,
                      Student.fullname,
                      Group.name,
                      Grade.date_of,
                      Grade.grade
                      ) \
        .select_from(Grade) \
        .join(Student) \
        .join(Discipline) \
        .join(Group) \
        .filter(and_(Discipline.id == discipline_id, Group.id == group_id, Grade.date_of == subquery)) \
        .order_by(desc(Grade.date_of)) \
        .all()
    return r

if __name__ == '__main__':
    pprint(select_1())
    pprint(select_2(6))
    pprint(select_3(4))
    pprint(select_4())
    pprint(select_5())
    pprint(select_6(2))
    pprint(select_7(3, 5))
    pprint(select_8(5))
    pprint(select_9(29))
    pprint(select_10(24, 5))
    pprint(select_11(24, 5))
    pprint(select_12(4, 2))


