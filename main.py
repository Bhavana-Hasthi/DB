# university_analytics.py
from sqlmodel import Session, select, create_engine
from university_db import University, Department, Student

engine = create_engine("sqlite:///university.db", echo=True)

# STUDENT FUNCTIONS

def get_all_students(session: Session):
    """Get all students"""
    try:
        students = session.exec(select(Student)).all()
        print(f"[INFO] Retrieved {len(students)} students.")
        return students
    except Exception as e:
        print(f"[ERROR] Failed to get students: {e}")
        return []

def get_student_by_id(session: Session, student_id: int):
    """Get student by ID"""
    try:
        student = session.get(Student, student_id)
        print(f"[INFO] Found student: {student}" if student else f"[INFO] No student found with ID {student_id}")
        return student
    except Exception as e:
        print(f"[ERROR] Failed to fetch student ID {student_id}: {e}")
        return None

def create_student(session: Session, name: str, year: int = None, dept_id: int = None):
    """Create new student"""
    try:
        new_student = Student(student_name=name, enrollment_year=year, department_id=dept_id)
        session.add(new_student)
        session.commit()
        session.refresh(new_student)
        print(f"[INFO] Created student: {new_student}")
        return new_student
    except Exception as e:
        session.rollback()
        print(f"[ERROR] Failed to create student: {e}")
        return None

def update_student(session: Session, student_id: int, name: str = None, year: int = None, dept_id: int = None):
    """Update student details"""
    try:
        student = session.get(Student, student_id)
        print(f"[INFO] Updating student: {student}")
        if not student:
            print(f"[INFO] No student found with ID {student_id}")
            return None
        if name:
            student.student_name = name
        if year:
            student.enrollment_year = year
        if dept_id:
            student.department_id = dept_id
        session.add(student)
        session.commit()
        session.refresh(student)
        print(f"[INFO] Updated student successfully: {student}")
        return student
    except Exception as e:
        session.rollback()
        print(f"[ERROR] Failed to update student {student_id}: {e}")
        return None

def delete_student(session: Session, student_id: int):
    """Delete student"""
    try:
        student = session.get(Student, student_id)
        if not student:
            print(f"[INFO] No student found with ID {student_id}")
            return False
        session.delete(student)
        session.commit()
        print(f"[INFO] Deleted student ID {student_id}")
        return True
    except Exception as e:
        session.rollback()
        print(f"[ERROR] Failed to delete student {student_id}: {e}")
        return False


# DEPARTMENT FUNCTIONS
def get_all_departments(session: Session):
    try:
        departments = session.exec(select(Department)).all()
        print(f"[INFO] Retrieved {len(departments)} departments.")
        return departments
    except Exception as e:
        print(f"[ERROR] Failed to get departments: {e}")
        return []

def create_department(session: Session, name: str, uni_id: int = None):
    try:
        new_dept = Department(department_name=name, university_id=uni_id)
        session.add(new_dept)
        session.commit()
        session.refresh(new_dept)
        print(f"[INFO] Created department: {new_dept}")
        return new_dept
    except Exception as e:
        session.rollback()
        print(f"[ERROR] Failed to create department: {e}")
        return None

# UNIVERSITY FUNCTIONS
def get_all_universities(session: Session):
    try:
        universities = session.exec(select(University)).all()
        print(f"[INFO] Retrieved {len(universities)} universities.")
        return universities
    except Exception as e:
        print(f"[ERROR] Failed to get universities: {e}")
        return []

def create_university(session: Session, name: str, location: str = None):
    try:
        new_uni = University(university_name=name, location=location)
        session.add(new_uni)
        session.commit()
        session.refresh(new_uni)
        print(f"[INFO] Created university: {new_uni}")
        return new_uni
    except Exception as e:
        session.rollback()
        print(f"[ERROR] Failed to create university: {e}")
        return None

# QUERY FUNCTIONS
def get_students_by_department(session: Session, dept_id: int):
    """Get all students in a specific department"""
    try:
        students = session.exec(select(Student).where(Student.department_id == dept_id)).all()
        print(f"[INFO] Retrieved {len(students)} students for department {dept_id}.")
        return students
    except Exception as e:
        print(f"[ERROR] Failed to get students for department {dept_id}: {e}")
        return []

def get_departments_by_university(session: Session, uni_id: int):
    """Get all departments in a specific university"""
    try:
        departments = session.exec(select(Department).where(Department.university_id == uni_id)).all()
        print(f"[INFO] Retrieved {len(departments)} departments for university {uni_id}.")
        return departments
    except Exception as e:
        print(f"[ERROR] Failed to get departments for university {uni_id}: {e}")
        return []

def get_students_with_details(session: Session):
    """Get students with joined department and university"""
    try:
        data = session.exec(select(Student).join(Department).join(University)).all()
        print(f"[INFO] Retrieved {len(data)} students with full details.")
        return data
    except Exception as e:
        print(f"[ERROR] Failed to get student details: {e}")
        return []

# TEST RUN
if __name__ == "__main__":
    with Session(engine) as session:
        students = get_students_by_department(session, 1)
        print(f"Students in Department 1: {students}")
