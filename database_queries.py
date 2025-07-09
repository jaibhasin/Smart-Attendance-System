"""
Database queries for the Smart Attendance System
This file contains all the SQL queries used in the application
"""

from myproject import app, db
from myproject.models import Student, Parent, Professor, Course, Admin, ClassRoom, Attendance, student_course
from werkzeug.security import generate_password_hash
from datetime import date, datetime
import os
import random

def insert_sample_data():
    """Insert sample data into the database"""
    with app.app_context():
        # Clear existing data to avoid unique constraint errors
        professors = [
            Professor('John', 'Smith', 'john.smith@university.edu', 'password123', '555-123-4567'),
            Professor('Emily', 'Johnson', 'emily.johnson@university.edu', 'password123', '555-234-5678'),
            Professor('Michael', 'Williams', 'michael.williams@university.edu', 'password123', '555-345-6789')
        ]
        
        for professor in professors:
            db.session.add(professor)
        
        # Commit to get professor IDs
        db.session.commit()
        
        # Add courses
        courses = [
            Course(course_name='Introduction to Computer Science', total_classes=30, teacher_id=1),
            Course(course_name='Data Structures and Algorithms', total_classes=25, teacher_id=1),
            Course(course_name='Database Systems', total_classes=28, teacher_id=2),
            Course(course_name='Web Development', total_classes=20, teacher_id=3),
            Course(course_name='Artificial Intelligence', total_classes=22, teacher_id=2)
        ]
        
        for course in courses:
            db.session.add(course)
        
        # Commit to get course IDs
        db.session.commit()
        
        # Add students
        students = [
            Student('Alice', 'Brown', 'alice.brown@university.edu', 'password123', 'Apt 101, University Ave', '555-987-6543', 'Computer Science'),
            Student('Bob', 'Davis', 'bob.davis@university.edu', 'password123', 'Apt 202, College St', '555-876-5432', 'Computer Science'),
            Student('Carol', 'Evans', 'carol.evans@university.edu', 'password123', 'Apt 303, Campus Rd', '555-765-4321', 'Information Technology'),
            Student('David', 'Garcia', 'david.garcia@university.edu', 'password123', 'Apt 404, Scholar Ln', '555-654-3210', 'Information Technology'),
            Student('Eva', 'Hernandez', 'eva.hernandez@university.edu', 'password123', 'Apt 505, Academic Blvd', '555-543-2109', 'Computer Science')
        ]
        
        for student in students:
            db.session.add(student)
        
        # Commit to get student IDs
        db.session.commit()
        
        # Add parents
        parents = [
            Parent('James', 'Brown', 'james.brown@email.com', 'password123', '555-111-2222'),
            Parent('Mary', 'Davis', 'mary.davis@email.com', 'password123', '555-222-3333'),
            Parent('Robert', 'Evans', 'robert.evans@email.com', 'password123', '555-333-4444'),
            Parent('Patricia', 'Garcia', 'patricia.garcia@email.com', 'password123', '555-444-5555'),
            Parent('Thomas', 'Hernandez', 'thomas.hernandez@email.com', 'password123', '555-555-6666')
        ]
        
        for parent in parents:
            db.session.add(parent)
        
        # Commit to get parent IDs
        db.session.commit()
        
        # Add admin
        admin = Admin(name='Admin User', email='admin@university.edu', role='system_admin')
        db.session.add(admin)
        db.session.commit()
        
        # Add classrooms
        classrooms = [
            ClassRoom(room_number='A101', professor_id=1, student_id=1, course_id=1),
            ClassRoom(room_number='A102', professor_id=1, student_id=2, course_id=2),
            ClassRoom(room_number='B201', professor_id=2, student_id=3, course_id=3),
            ClassRoom(room_number='B202', professor_id=3, student_id=4, course_id=4),
            ClassRoom(room_number='C301', professor_id=2, student_id=5, course_id=5)
        ]
        
        for classroom in classrooms:
            db.session.add(classroom)
        
        # Commit classrooms
        db.session.commit()
        
        # Add student-course enrollments (using the student_course table)
        # Student 1 (Alice) enrolled in courses 1, 2, and 3
        db.session.execute(student_course.insert().values(student_id=1, course_id=1))
        db.session.execute(student_course.insert().values(student_id=1, course_id=2))
        db.session.execute(student_course.insert().values(student_id=1, course_id=3))
        
        # Student 2 (Bob) enrolled in courses 2 and 4
        db.session.execute(student_course.insert().values(student_id=2, course_id=2))
        db.session.execute(student_course.insert().values(student_id=2, course_id=4))
        
        # Student 3 (Carol) enrolled in courses 3 and 5
        db.session.execute(student_course.insert().values(student_id=3, course_id=3))
        db.session.execute(student_course.insert().values(student_id=3, course_id=5))
        
        # Student 4 (David) enrolled in courses 1, 4, and 5
        db.session.execute(student_course.insert().values(student_id=4, course_id=1))
        db.session.execute(student_course.insert().values(student_id=4, course_id=4))
        db.session.execute(student_course.insert().values(student_id=4, course_id=5))
        
        # Student 5 (Eva) enrolled in courses 2, 3, and 5
        db.session.execute(student_course.insert().values(student_id=5, course_id=2))
        db.session.execute(student_course.insert().values(student_id=5, course_id=3))
        db.session.execute(student_course.insert().values(student_id=5, course_id=5))
        
        db.session.commit()
        
        # Add attendance records for all student-course enrollments
        attendance_records = []
        
        # Common dates for all courses
        class_dates = [
            date(2025, 5, 1), date(2025, 5, 3), date(2025, 5, 5), date(2025, 5, 8),
            date(2025, 5, 10), date(2025, 5, 12), date(2025, 5, 15), date(2025, 5, 17)
        ]
        
        # Student 1 (Alice) enrolled in courses 1, 2, and 3
        for course_id in [1, 2, 3]:
            for class_date in class_dates:
                # 80% attendance rate with random absences
                status = 'Present' if random.random() < 0.8 else 'Absent'
                attendance_records.append(Attendance(date=class_date, status=status, student_id=1, course_id=course_id))
        
        # Student 2 (Bob) enrolled in courses 2 and 4
        for course_id in [2, 4]:
            for class_date in class_dates:
                # 75% attendance rate with random absences
                status = 'Present' if random.random() < 0.75 else 'Absent'
                attendance_records.append(Attendance(date=class_date, status=status, student_id=2, course_id=course_id))
        
        # Student 3 (Carol) enrolled in courses 3 and 5
        for course_id in [3, 5]:
            for class_date in class_dates:
                # 85% attendance rate with random absences
                status = 'Present' if random.random() < 0.85 else 'Absent'
                attendance_records.append(Attendance(date=class_date, status=status, student_id=3, course_id=course_id))
        
        # Student 4 (David) enrolled in courses 1, 4, and 5
        for course_id in [1, 4, 5]:
            for class_date in class_dates:
                # 70% attendance rate with random absences
                status = 'Present' if random.random() < 0.7 else 'Absent'
                attendance_records.append(Attendance(date=class_date, status=status, student_id=4, course_id=course_id))
        
        # Student 5 (Eva) enrolled in courses 2, 3, and 5
        for course_id in [2, 3, 5]:
            for class_date in class_dates:
                # 90% attendance rate with random absences
                status = 'Present' if random.random() < 0.9 else 'Absent'
                attendance_records.append(Attendance(date=class_date, status=status, student_id=5, course_id=course_id))
        
        for attendance in attendance_records:
            db.session.add(attendance)
        
        # Final commit
        db.session.commit()
        print("Sample data inserted successfully!")

def query_all_students():
    """Query all students"""
    with app.app_context():
        students = Student.query.all()
        return students

def query_all_professors():
    """Query all professors"""
    with app.app_context():
        professors = Professor.query.all()
        return professors

def query_all_courses():
    """Query all courses"""
    with app.app_context():
        courses = Course.query.all()
        return courses

def query_student_attendance(student_id):
    """Query attendance for a specific student"""
    with app.app_context():
        attendance = Attendance.query.filter_by(student_id=student_id).all()
        return attendance

def query_course_attendance(course_id):
    """Query attendance for a specific course"""
    with app.app_context():
        attendance = Attendance.query.filter_by(course_id=course_id).all()
        return attendance

def query_professor_courses(professor_id):
    """Query courses taught by a specific professor"""
    with app.app_context():
        courses = Course.query.filter_by(teacher_id=professor_id).all()
        return courses

def query_classroom_details():
    """Query all classroom details with related information"""
    with app.app_context():
        classrooms = ClassRoom.query.all()
        classroom_details = []
        
        for classroom in classrooms:
            professor = Professor.query.get(classroom.professor_id)
            student = Student.query.get(classroom.student_id)
            course = Course.query.get(classroom.course_id)
            
            classroom_details.append({
                'room_number': classroom.room_number,
                'professor': f"{professor.first_name} {professor.last_name}",
                'student': f"{student.first_name} {student.last_name}",
                'course': course.course_name
            })
        
        return classroom_details

def query_attendance_stats():
    """Query attendance statistics"""
    with app.app_context():
        total_attendance = Attendance.query.count()
        present_count = Attendance.query.filter_by(status='Present').count()
        absent_count = Attendance.query.filter_by(status='Absent').count()
        
        return {
            'total': total_attendance,
            'present': present_count,
            'absent': absent_count,
            'present_percentage': (present_count / total_attendance * 100) if total_attendance > 0 else 0
        }
