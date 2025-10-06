# university_db.py
from typing import Optional, List
from sqlmodel import SQLModel, Field, Relationship, create_engine, Session

# -----------------------------
# Universities Table
# -----------------------------
class University(SQLModel, table=True):
    university_id: Optional[int] = Field(default=None, primary_key=True)
    university_name: str
    location: Optional[str] = None

    departments: List["Department"] = Relationship(back_populates="university")


# -----------------------------
# Departments Table
# -----------------------------
class Department(SQLModel, table=True):
    department_id: Optional[int] = Field(default=None, primary_key=True)
    department_name: str
    university_id: Optional[int] = Field(default=None, foreign_key="university.university_id")

    university: Optional[University] = Relationship(back_populates="departments")
    students: List["Student"] = Relationship(back_populates="department")


# -----------------------------
# Students Table
# -----------------------------
class Student(SQLModel, table=True):
    student_id: Optional[int] = Field(default=None, primary_key=True)
    student_name: str
    enrollment_year: Optional[int] = None
    department_id: Optional[int] = Field(default=None, foreign_key="department.department_id")

    department: Optional[Department] = Relationship(back_populates="students")


# -----------------------------
# Create SQLite Database
# -----------------------------
sqlite_file_name = "D:/university_db_project/university.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"

engine = create_engine(sqlite_url, echo=True)

# Create tables
SQLModel.metadata.create_all(engine)


# -----------------------------
# Insert Sample Data
# -----------------------------
# with Session(engine) as session:
#     # Universities
#     abc = University(university_name="ABC University", location="Delhi")
#     xyz = University(university_name="XYZ University", location="Mumbai")
#     session.add_all([abc, xyz])
#     session.commit()

#     # Departments
#     cs = Department(department_name="Computer Science", university_id=abc.university_id)
#     mech = Department(department_name="Mechanical Engineering", university_id=abc.university_id)
#     ee = Department(department_name="Electrical Engineering", university_id=xyz.university_id)
#     session.add_all([cs, mech, ee])
#     session.commit()

#     # Students
#     s1 = Student(student_name="Bharathi", enrollment_year=2023, department_id=cs.department_id)
#     s2 = Student(student_name="Rani", enrollment_year=2022, department_id=mech.department_id)
#     s3 = Student(student_name="Sneha", enrollment_year=2023, department_id=ee.department_id)
#     session.add_all([s1, s2, s3])
#     session.commit()

# print("Database and sample data created successfully!")
