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
@app.route("/")
def home():
    return "University Student Management API is running."

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
        location = data.get("location", "Tirupati")  # Default location

        if not all([student_name, year, department_name, university_name]):
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

# FLEXIBLE UPDATE STUDENT
@app.route("/students/update", methods=["PUT"])
def flexible_update_student():
    try:
        data = request.json
        print(f"🔄 Received update data: {data}")

        name = data.get("name")
        department_name = data.get("department")
        university_name = data.get("university")
        year = data.get("year")
        student_id = data.get("student_id")

        if not any([student_id, name, department_name, university_name, year]):
            return jsonify({"status": "failed", "message": "Provide at least one identifying field"}), 400

        with get_session() as session:
            student = None

            # 🎯 Prefer ID if given
            if student_id:
                student = session.get(Student, int(student_id))
            else:
                query = select(Student)
                if name:
                    query = query.where(Student.student_name.ilike(f"%{name}%"))
                if year:
                    query = query.where(Student.enrollment_year == year)
                if department_name and university_name:
                    uni = get_university_by_name(university_name)
                    if uni:
                        dept = get_department_by_name(department_name, uni.university_id)
                        if dept:
                            query = query.where(Student.department_id == dept.department_id)
                student = session.exec(query).first()

            if not student:
                return jsonify({"status": "failed", "message": "Student not found"}), 404

            # 🧩 Update fields
            if "new_name" in data:
                student.student_name = data["new_name"]
            if "new_year" in data:
                student.enrollment_year = data["new_year"]
            if "new_department" in data and "new_university" in data:
                uni = get_university_by_name(data["new_university"])
                if uni:
                    dept = get_department_by_name(data["new_department"], uni.university_id)
                    if dept:
                        student.department_id = dept.department_id

            session.add(student)
            session.commit()
            session.refresh(student)

            print("✅ Student updated successfully")
            return jsonify({"status": "success", "message": "Student updated", "student": student.dict()}), 200

    except Exception as e:
        print(f"❌ Error updating student: {e}")
        return jsonify({"status": "failed", "message": str(e)}), 500

# FLEXIBLE DELETE STUDENT
@app.route("/students/delete", methods=["DELETE"])
def flexible_delete_student():
    try:
        data = request.json
        print(f"🗑️ Received delete data: {data}")

        student_id = data.get("student_id")
        name = data.get("name")
        department_name = data.get("department")
        university_name = data.get("university")
        year = data.get("year")

        with get_session() as session:
            student = None

            if student_id:
                student = session.get(Student, int(student_id))
            else:
                query = select(Student)
                if name:
                    query = query.where(Student.student_name.ilike(f"%{name}%"))
                if year:
                    query = query.where(Student.enrollment_year == year)
                if department_name and university_name:
                    uni = get_university_by_name(university_name)
                    if uni:
                        dept = get_department_by_name(department_name, uni.university_id)
                        if dept:
                            query = query.where(Student.department_id == dept.department_id)
                student = session.exec(query).first()

            if not student:
                return jsonify({"status": "failed", "message": "Student not found"}), 404

            session.delete(student)
            session.commit()
            print("✅ Student deleted successfully")

            return jsonify({"status": "success", "message": f"Deleted student '{student.student_name}'"}), 200

    except Exception as e:
        print(f"❌ Error deleting student: {e}")
        return jsonify({"status": "failed", "message": str(e)}), 500

# SEARCH STUDENT
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

# RUN SERVER
if __name__ == "__main__":
    app.run(debug=True, use_reloader=False)
