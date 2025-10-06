from sqlmodel import SQLModel, Session, create_engine, select
from university_db import University, Department, Student  # Import your models

# -----------------------------
# Connect to existing database
# -----------------------------
sqlite_file_name = "D:/university_db_project/university.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"

engine = create_engine(sqlite_url, echo=True)

# -----------------------------
# CRUD Operations
# -----------------------------
with Session(engine) as session:
    
    # -----------------------------
    # SELECT - Get all students
    # -----------------------------
    print("All students:")
    students = session.exec(select(Student)).all()
    for s in students:
        print(f"{s.student_id} | {s.student_name} | Department ID: {s.department_id} | Year: {s.enrollment_year}")

    # -----------------------------
    # UPDATE - Change student name
    # -----------------------------
    student_to_update = session.get(Student, 1)  # Get student with ID 1
    if student_to_update:
        student_to_update.student_name = "Monica Sharma"
        session.add(student_to_update)
        session.commit()
        print("\nUpdated student 1 name successfully!")

    # -----------------------------
    # DELETE - Remove a student
    # -----------------------------
    student_to_delete = session.get(Student, 2)  # Delete student with ID 2
    if student_to_delete:
        session.delete(student_to_delete)
        session.commit()
        print("\nDeleted student 2 successfully!")

    # -----------------------------
    # SELECT after update & delete
    # -----------------------------
    print("\nStudents after update and delete:")
    students = session.exec(select(Student)).all()
    for s in students:
        print(f"{s.student_id} | {s.student_name} | Department ID: {s.department_id} | Year: {s.enrollment_year}")
