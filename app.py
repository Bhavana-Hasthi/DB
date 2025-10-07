from flask import Flask, request, jsonify
from sqlmodel import Session, select, create_engine
from university_db import University, Department, Student

app = Flask(__name__)
DATABASE_URL = "sqlite:///university.db"
engine = create_engine(DATABASE_URL, echo=True)

# DB SESSION
def get_session():
    return Session(engine)

# HELPER FUNCTIONS

def get_university_by_name(name: str):
    with get_session() as session:
        return session.exec(
            select(University).where(University.university_name == name)
        ).first()


def add_university_entry(name: str, location: str):
    with get_session() as session:
        uni = University(university_name=name, location=location)
        session.add(uni)
        session.commit()
        session.refresh(uni)
        return uni


def get_department_by_name(dept_name: str, uni_id: int):
    with get_session() as session:
        return session.exec(
            select(Department)
            .where(Department.department_name == dept_name)
            .where(Department.university_id == uni_id)
        ).first()


def add_department_entry(dept_name: str, uni_id: int):
    with get_session() as session:
        dept = Department(department_name=dept_name, university_id=uni_id)
        session.add(dept)
        session.commit()
        session.refresh(dept)
        return dept


def get_student_by_details(name: str, year: int, dept_id: int):
    with get_session() as session:
        return session.exec(
            select(Student)
            .where(Student.student_name == name)
            .where(Student.enrollment_year == year)
            .where(Student.department_id == dept_id)
        ).first()


def add_student_entry_to_db(name: str, year: int, dept_id: int):
    with get_session() as session:
        student = Student(
            student_name=name,
            enrollment_year=year,
            department_id=dept_id
        )
        session.add(student)
        session.commit()
        session.refresh(student)
        return student

# ROUTES

# ADD STUDENT
@app.route("/students/full_add", methods=["POST"])
def add_student_entry():
    try:
        print("Adding student entry...")
        data = request.json
        print(f"Received data: {data}")

        student_name = data.get("name")
        year = data.get("year")
        department_name = data.get("department")
        university_name = data.get("university")
        location = data.get("location")

        if not all([student_name, year, department_name, university_name, location]):
            return jsonify({"status": "failed", "message": "All fields are required"}), 400

        university_obj = get_university_by_name(university_name)
        if university_obj:
            university_id = university_obj.university_id
        else:
            university_obj = add_university_entry(university_name, location)
            university_id = university_obj.university_id

        department_obj = get_department_by_name(department_name, university_id)
        if department_obj:
            department_id = department_obj.department_id
        else:
            department_obj = add_department_entry(department_name, university_id)
            department_id = department_obj.department_id

        existing_student = get_student_by_details(student_name, year, department_id)
        if existing_student:
            return jsonify({
                "status": "failed",
                "message": f"Student '{student_name}' already exists in this department and year."
            }), 409

        add_student_entry_to_db(student_name, year, department_id)
        print("✅ Student added successfully")

        return jsonify({"status": "success", "message": "Student added successfully"}), 200

    except Exception as e:
        print(f"❌ Error occurred: {e}")
        return jsonify({"status": "failed", "message": str(e)}), 500

# UPDATE STUDENT
@app.route("/students/update/<int:student_id>", methods=["PUT"])
def update_student(student_id):
    try:
        print(f"Updating student with ID {student_id}")
        data = request.json
        print(f"Received update data: {data}")

        with get_session() as session:
            student = session.get(Student, student_id)
            if not student:
                return jsonify({"status": "failed", "message": "Student not found"}), 404

            if "name" in data:
                student.student_name = data["name"]
            if "year" in data:
                student.enrollment_year = data["year"]
            if "department_id" in data:
                student.department_id = data["department_id"]

            session.add(student)
            session.commit()
            session.refresh(student)

            print("✅ Student updated successfully")
            return jsonify({"status": "success", "message": "Student updated", "student": student.dict()}), 200

    except Exception as e:
        print(f"❌ Error updating student: {e}")
        return jsonify({"status": "failed", "message": str(e)}), 500

# DELETE STUDENT
@app.route("/students/delete/<int:student_id>", methods=["DELETE"])
def delete_student(student_id):
    try:
        print(f"Deleting student with ID {student_id}")
        with get_session() as session:
            student = session.get(Student, student_id)
            if not student:
                return jsonify({"status": "failed", "message": "Student not found"}), 404

            session.delete(student)
            session.commit()
            print("✅ Student deleted successfully")
            return jsonify({"status": "success", "message": "Student deleted"}), 200

    except Exception as e:
        print(f"❌ Error deleting student: {e}")
        return jsonify({"status": "failed", "message": str(e)}), 500

# SEARCH STUDENT BY NAME OR ID
@app.route("/students/search", methods=["GET"])
def search_student():
    try:
        name = request.args.get("name")
        student_id = request.args.get("id")

        print(f"Searching student by name='{name}' or id='{student_id}'")

        with get_session() as session:
            if student_id:
                student = session.get(Student, int(student_id))
                if student:
                    return jsonify({"status": "success", "student": student.dict()}), 200
                else:
                    return jsonify({"status": "failed", "message": "Student not found"}), 404

            elif name:
                students = session.exec(
                    select(Student).where(Student.student_name.ilike(f"%{name}%"))
                ).all()

                if students:
                    return jsonify({
                        "status": "success",
                        "results": [s.dict() for s in students]
                    }), 200
                else:
                    return jsonify({"status": "failed", "message": "No students found with this name"}), 404

            else:
                return jsonify({"status": "failed", "message": "Provide 'name' or 'id' as query param"}), 400

    except Exception as e:
        print(f"❌ Error searching student: {e}")
        return jsonify({"status": "failed", "message": str(e)}), 500

# 🚀 Run Server
if __name__ == "__main__":
    app.run(debug=True, use_reloader=False)
