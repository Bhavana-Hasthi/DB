from sqlmodel import SQLModel, Session, select, create_engine
from university_db import University, Department, Student

# Database Setup 
DATABASE_URL = "sqlite:///university.db"
engine = create_engine(DATABASE_URL, echo=True)  # echo=True shows SQL logs
SQLModel.metadata.create_all(engine)


#  Generic CRUD Functions 
def safe_action(action_name, func, *args, **kwargs):
    """Utility to wrap DB actions with try/except and logs."""
    try:
        result = func(*args, **kwargs)
        if isinstance(result, list):
            print(f"[INFO] Retrieved {len(result)} {action_name}.")
        else:
            print(f"[INFO] {action_name} executed successfully.")
        return result
    except Exception as e:
        print(f"[ERROR] Failed to {action_name}: {e}")
        return [] if "get" in action_name.lower() else None


def create_entry(session, model, **kwargs):
    return safe_action(
        f"create {model.__name__}",
        lambda: _create(session, model, **kwargs)
    )


def _create(session, model, **kwargs):
    obj = model(**kwargs)
    session.add(obj)
    session.commit()
    session.refresh(obj)
    return obj


def get_all(session, model):
    return safe_action(f"get all {model.__name__}", lambda: session.exec(select(model)).all())


def get_students_by_department(session, dept_id):
    return safe_action(
        f"get students in department {dept_id}",
        lambda: session.exec(select(Student).where(Student.department_id == dept_id)).all()
    )


#  Main Script 
with Session(engine) as session:

    # Create initial data only if database empty
    if not get_all(session, University):
        print("\n[INFO] Creating sample data...")
        uni1 = create_entry(session, University, university_name="ABC University", location="Delhi")
        uni2 = create_entry(session, University, university_name="XYZ University", location="Mumbai")

        dept1 = create_entry(session, Department, department_name="Computer Science", university_id=uni1.university_id)
        dept2 = create_entry(session, Department, department_name="Physics", university_id=uni2.university_id)

        create_entry(session, Student, student_name="Monica Sharma", enrollment_year=2024, department_id=dept1.department_id)
        create_entry(session, Student, student_name="Ravi Kumar", enrollment_year=2023, department_id=dept1.department_id)
        create_entry(session, Student, student_name="Sneha Patel", enrollment_year=2024, department_id=dept2.department_id)

    # -------- OUTPUT SECTION --------
    print("\n========================")
    print(" All Students ")
    print("========================")
    students = get_all(session, Student)
    print(f"Students: {students}\n")

    print("========================")
    print(" Students in Department 1 ")
    print("========================")
    dept_students = get_students_by_department(session, 1)
    print(f"Students in Department 1: {dept_students}\n")

    print("========================")
    print(" All Departments ")
    print("========================")
    departments = get_all(session, Department)
    print(f"Departments: {departments}\n")

    print("========================")
    print(" All Universities ")
    print("========================")
    universities = get_all(session, University)
    print(f"Universities: {universities}\n")
