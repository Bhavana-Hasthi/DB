-- queries.sql

-- Get all students with their department and university
SELECT s.student_name, s.enrollment_year, d.department_name, u.university_name
FROM Students s
JOIN Departments d ON s.department_id = d.department_id
JOIN Universities u ON d.university_id = u.university_id;

-- List all universities
SELECT * FROM Universities;

-- List all departments
SELECT * FROM Departments;

-- List all students
SELECT * FROM Students;
