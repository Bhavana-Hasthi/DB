# crud_functions.py
from sqlmodel import Session, select
from university_db import University, Department, Student
from university_db import engine

# -----------------------------
# Student Functions
# -----------------------------
def get_all_students(session: Session):
    """Get all students"""
    return session.exec(select(Student)).all()

def get_student_by_id(session: Session, student_id: int):
    """Get student by ID"""
    return session.get(Student, student_id)

def create_student(session: Session, name: str, year: int = None, dept_id: int = None):
    """Create new student"""
    student = Student(student_name=name, enrollment_year=year, department_id=dept_id)
    session.add(student)
    session.commit()
    session.refresh(student)
    return student

def update_student(session: Session, student_id: int, name: str = None, year: int = None, dept_id: int = None):
    """Update student details"""
    student = session.get(Student, student_id)
    if student:
        if name:
            student.student_name = name
        if year:
            student.enrollment_year = year
        if dept_id:
            student.department_id = dept_id
        session.add(student)
        session.commit()
        session.refresh(student)
    return student

def delete_student(session: Session, student_id: int):
    """Delete student"""
    student = session.get(Student, student_id)
    if student:
        session.delete(student)
        session.commit()
        return True
    return False

# -----------------------------
# Department Functions
# -----------------------------
def get_all_departments(session: Session):
    """Get all departments"""
    return session.exec(select(Department)).all()

def get_department_by_id(session: Session, department_id: int):
    """Get department by ID"""
    return session.get(Department, department_id)

def create_department(session: Session, name: str, uni_id: int = None):
    """Create new department"""
    department = Department(department_name=name, university_id=uni_id)
    session.add(department)
    session.commit()
    session.refresh(department)
    return department

def update_department(session: Session, department_id: int, name: str = None, uni_id: int = None):
    """Update department details"""
    department = session.get(Department, department_id)
    if department:
        if name:
            department.department_name = name
        if uni_id:
            department.university_id = uni_id
        session.add(department)
        session.commit()
        session.refresh(department)
    return department

def delete_department(session: Session, department_id: int):
    """Delete department"""
    department = session.get(Department, department_id)
    if department:
        session.delete(department)
        session.commit()
        return True
    return False

# -----------------------------
# University Functions
# -----------------------------
def get_all_universities(session: Session):
    """Get all universities"""
    return session.exec(select(University)).all()

def get_university_by_id(session: Session, university_id: int):
    """Get university by ID"""
    return session.get(University, university_id)

def create_university(session: Session, name: str, location: str = None):
    """Create new university"""
    university = University(university_name=name, location=location)
    session.add(university)
    session.commit()
    session.refresh(university)
    return university

def update_university(session: Session, university_id: int, name: str = None, location: str = None):
    """Update university details"""
    university = session.get(University, university_id)
    if university:
        if name:
            university.university_name = name
        if location:
            university.location = location
        session.add(university)
        session.commit()
        session.refresh(university)
    return university

def delete_university(session: Session, university_id: int):
    """Delete university"""
    university = session.get(University, university_id)
    if university:
        session.delete(university)
        session.commit()
        return True
    return False

# -----------------------------
# Query Functions
# -----------------------------
def get_students_with_details(session: Session):
    """Get students with department and university details"""
    statement = select(Student).join(Department).join(University)
    return session.exec(statement).all()

def get_departments_by_university(session: Session, university_id: int):
    """Get all departments of a specific university"""
    statement = select(Department).where(Department.university_id == university_id)
    return session.exec(statement).all()

def get_students_by_department(session: Session, department_id: int):
    """Get all students in a specific department"""
    statement = select(Student).where(Student.department_id == department_id)
    return session.exec(statement).all()
# all_students=get_all_students(session=Session(engine))
# print(f"All Students: {all_students}")

department= get_students_by_department(session=Session(engine), department_id=1)
print(f"Students in Department 1:{department}")
