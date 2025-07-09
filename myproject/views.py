from flask import render_template, redirect, url_for, request, Blueprint, flash, jsonify, session
from myproject import db, app
from flask_login import login_user, current_user, logout_user, login_required
from myproject.models import Student, Parent, Professor, Course, Admin, ClassRoom, Attendance, student_course
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps

@app.route('/')
@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/student/login', methods=['GET', 'POST'])
def student_login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        student = Student.query.filter_by(email=email).first()
        
        if student and check_password_hash(student.password_hash, password):
            login_user(student)
            return redirect(url_for('students'))
        else:
            flash('Invalid email or password')
            return redirect(url_for('student_login'))
    return render_template('login_student.html')

@app.route('/parent/login', methods=['GET', 'POST'])
def parent_login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        parent = Parent.query.filter_by(email=email).first()
        
        if parent and check_password_hash(parent.password_hash, password):
            login_user(parent)
            return redirect(url_for('parent'))
        else:
            flash('Invalid email or password')
            return redirect(url_for('parent_login'))
    return render_template('login_parent.html')

@app.route('/teacher/login', methods=['GET', 'POST'])
def teacher_login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        professor = Professor.query.filter_by(email=email).first()
        
        if professor and check_password_hash(professor.password_hash, password):
            login_user(professor)
            return redirect(url_for('teacher'))
        else:
            flash('Invalid email or password')
            return redirect(url_for('teacher_login'))
    return render_template('login_teacher.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out successfully', 'success')
    return redirect(url_for('login'))

@app.route('/students')
@login_required
def students():
    if not isinstance(current_user, Student):
        flash('Access Denied: You must be a student to access this page', 'error')
        return redirect(url_for('login'))
    
    # Get student courses
    student_courses = Course.query.join(student_course).filter(student_course.c.student_id == current_user.student_id).all()
    
    # Get attendance records for the student
    attendance_records = Attendance.query.filter_by(student_id=current_user.student_id).all()
    
    # Calculate attendance statistics
    course_attendance = {}
    overall_attended = 0
    overall_total = 0
    
    for course in student_courses:
        course_records = [record for record in attendance_records if record.course_id == course.course_id]
        attended = sum(1 for record in course_records if record.status == 'Present')
        total = len(course_records)
        overall_attended += attended
        overall_total += total
        
        if total > 0:
            percentage = (attended / total) * 100
        else:
            percentage = 0
            
        # Get professor name for this course
        professor = Professor.query.get(course.teacher_id)
        professor_name = f"Prof. {professor.first_name} {professor.last_name}" if professor else "Not Assigned"
        
        # Get last attended date
        last_attended = None
        present_records = [record for record in course_records if record.status == 'Present']
        if present_records:
            last_attended = max(present_records, key=lambda x: x.date).date
        
        course_attendance[course.course_id] = {
            'course': course,
            'attended': attended,
            'total': total,
            'percentage': percentage,
            'professor': professor_name,
            'last_attended': last_attended,
            'status': 'good' if percentage >= 75 else ('warning' if percentage >= 60 else 'danger')
        }
    
    # Calculate overall attendance percentage
    overall_percentage = (overall_attended / overall_total) * 100 if overall_total > 0 else 0
    
    return render_template('students_fixed.html', 
                           student=current_user,
                           course_attendance=course_attendance,
                           overall_percentage=overall_percentage,
                           now=datetime.now())

@app.route('/parent')
@login_required
def parent():
    if not isinstance(current_user, Parent):
        flash('Access Denied: You must be a parent to access this page', 'error')
        return redirect(url_for('login'))
    
    # Get parent's children (students)
    # For now, we'll assume each parent has one child with the same last name
    children = Student.query.filter_by(last_name=current_user.last_name).all()
    
    children_data = []
    for child in children:
        # Get student courses
        student_courses = Course.query.join(student_course).filter(student_course.c.student_id == child.student_id).all()
        
        # Get attendance records for the student
        attendance_records = Attendance.query.filter_by(student_id=child.student_id).all()
        
        # Calculate attendance statistics
        course_attendance = {}
        overall_attended = 0
        overall_total = 0
        
        for course in student_courses:
            course_records = [record for record in attendance_records if record.course_id == course.course_id]
            attended = sum(1 for record in course_records if record.status == 'Present')
            total = len(course_records)
            overall_attended += attended
            overall_total += total
            
            if total > 0:
                percentage = (attended / total) * 100
            else:
                percentage = 0
                
            # Get professor name for this course
            professor = Professor.query.get(course.teacher_id)
            professor_name = f"Prof. {professor.first_name} {professor.last_name}" if professor else "Not Assigned"
            
            # Get last attended date
            last_attended = None
            present_records = [record for record in course_records if record.status == 'Present']
            if present_records:
                last_attended = max(present_records, key=lambda x: x.date).date
            
            course_attendance[course.course_id] = {
                'course': course,
                'attended': attended,
                'total': total,
                'percentage': percentage,
                'professor': professor_name,
                'last_attended': last_attended,
                'status': 'good' if percentage >= 75 else ('warning' if percentage >= 60 else 'danger')
            }
        
        # Calculate overall attendance percentage
        overall_percentage = (overall_attended / overall_total) * 100 if overall_total > 0 else 0
        
        children_data.append({
            'student': child,
            'course_attendance': course_attendance,
            'overall_percentage': overall_percentage
        })
    
    return render_template('parent_fixed.html', 
                           parent=current_user,
                           children_data=children_data,
                           now=datetime.now())

@app.route('/teacher/attendance/<course_id>', methods=['GET', 'POST'])
@login_required
def mark_attendance(course_id):
    if not isinstance(current_user, Professor):
        flash('Access Denied: You must be a teacher to access this page', 'error')
        return redirect(url_for('login'))
    
    course1 = Course.query.get(course_id)
    if not course1:
        flash("Course Not Found", 'error')
        return redirect(url_for('teacher'))
    
    enrolled_students = Student.query.join(student_course).filter(student_course.c.course_id == course1.course_id).all()
    students_attendance = []
    
    # Get all unique dates for this course
    attendance_dates = db.session.query(Attendance.date).filter_by(course_id=course1.course_id).distinct().order_by(Attendance.date.desc()).all()
    attendance_dates = [date[0] for date in attendance_dates]
    
    for student in enrolled_students:
        records = Attendance.query.filter_by(student_id=student.student_id, course_id=course1.course_id).all()
        attendance_by_date = {record.date: record.status for record in records}
        students_attendance.append({
            'student': student,
            'attendance_by_date': attendance_by_date
        })
    
    if request.method == 'POST':
        date = datetime.strptime(request.form['date'], '%Y-%m-%d').date()
        
        # Check if attendance already exists for this date
        existing_attendance = Attendance.query.filter_by(course_id=course1.course_id, date=date).first()
        if existing_attendance:
            flash('Attendance for this date has already been marked', 'error')
            return redirect(url_for('mark_attendance', course_id=course_id))
        
        # Create new attendance records
        for student in enrolled_students:
            status = request.form.get(f'status_{student.student_id}')
            if status:
                attendance = Attendance(
                    date=date,
                    status=status,
                    student_id=student.student_id,
                    course_id=course1.course_id
                )
                db.session.add(attendance)
        
        try:
            db.session.commit()
            flash('Attendance marked successfully!', 'success')
        except Exception as e:
            db.session.rollback()
            flash('Error marking attendance. Please try again.', 'error')
        
        return redirect(url_for('mark_attendance', course_id=course_id))
    
    return render_template('mark_attendance.html', 
                         course=course1, 
                         students=students_attendance, 
                         dates=attendance_dates,
                         today=datetime.now().strftime('%Y-%m-%d'))

@app.route('/teacher')
@login_required
def teacher():
    if not isinstance(current_user, Professor):
        flash('Access Denied: You must be a teacher to access this page', 'error')
        return redirect(url_for('login'))
    
    # Get courses taught by this professor
    courses = Course.query.filter_by(teacher_id=current_user.professor_id).all()
    
    course_data = []
    for course in courses:
        # Get students enrolled in this course
        enrolled_students = Student.query.join(student_course).filter(student_course.c.course_id == course.course_id).all()
        
        # Get attendance records for this course
        attendance_records = Attendance.query.filter_by(course_id=course.course_id).all()
        
        # Calculate attendance statistics
        student_attendance = {}
        total_attended = 0
        total_classes = 0
        
        for student in enrolled_students:
            student_records = [record for record in attendance_records if record.student_id == student.student_id]
            attended = sum(1 for record in student_records if record.status == 'Present')
            total = len(student_records)
            total_attended += attended
            total_classes += total
            
            if total > 0:
                percentage = (attended / total) * 100
            else:
                percentage = 0
            
            # Get last attended date
            last_attended = None
            present_records = [record for record in student_records if record.status == 'Present']
            if present_records:
                last_attended = max(present_records, key=lambda x: x.date).date
            
            student_attendance[student.student_id] = {
                'student': student,
                'attended': attended,
                'total': total,
                'percentage': percentage,
                'last_attended': last_attended,
                'status': 'good' if percentage >= 75 else ('warning' if percentage >= 60 else 'danger')
            }
        
        # Calculate overall course attendance percentage
        course_percentage = (total_attended / total_classes) * 100 if total_classes > 0 else 0
        
        course_data.append({
            'course': course,
            'student_attendance': student_attendance,
            'enrolled_count': len(enrolled_students),
            'course_percentage': course_percentage
        })
    
    return render_template('teacher_fixed.html', 
                           professor=current_user,
                           course_data=course_data,
                           now=datetime.now())

# Admin authentication decorator
def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'admin_id' not in session:
            flash('Please log in as admin first', 'error')
            return redirect(url_for('admin_login'))
        return f(*args, **kwargs)
    return decorated_function

@app.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        email = request.form.get('email')
        admin = Admin.query.filter_by(email=email).first()
        
        if admin:
            session['admin_id'] = admin.admin_id
            flash('Logged in successfully as admin', 'success')
            return redirect(url_for('admin_dashboard'))
        else:
            flash('Invalid admin credentials', 'error')
            return redirect(url_for('admin_login'))
    return render_template('admin_login.html')

@app.route('/admin/logout')
def admin_logout():
    if 'admin_id' in session:
        session.pop('admin_id', None)
        flash('Logged out successfully', 'success')
    return redirect(url_for('login'))
@app.route('/admin')
@app.route('/admin/dashboard')
@admin_required
def admin_dashboard():
    stats = {
        'students': Student.query.count(),
        'professors': Professor.query.count(),
        'courses': Course.query.count(),
        'attendance': Attendance.query.count()
    }
    return render_template('admin_dashboard.html', stats=stats)

@app.route('/admin/students')
@admin_required
def admin_students():
    students = Student.query.all()
    return render_template('admin_students.html', students=students)

@app.route('/admin/professors')
@admin_required
def admin_professors():
    professors = Professor.query.all()
    return render_template('admin_professors.html', professors=professors)

@app.route('/admin/courses')
@admin_required
def admin_courses():
    # Get all courses with their enrolled students
    courses = Course.query.all()
    
    # For each course, get the enrolled students
    for course in courses:
        # Get students enrolled in this course via the junction table
        enrolled_students = db.session.query(Student).join(student_course).filter(student_course.c.course_id == course.course_id).all()
        course.students = enrolled_students
    
    return render_template('admin_courses.html', courses=courses)

@app.route('/admin/attendance')
@admin_required
def admin_attendance():
    attendance_records = Attendance.query.all()
    # Get all professors and create a dictionary for quick lookup
    all_professors = Professor.query.all()
    professors = {prof.professor_id: prof for prof in all_professors}
    # Get all courses for filtering
    courses = Course.query.all()
    return render_template('admin_attendance.html', attendance_records=attendance_records, professors=professors, courses=courses)

@app.route('/admin/classrooms')
@admin_required
def admin_classrooms():
    classrooms = ClassRoom.query.all()
    return render_template('admin_classrooms.html', classrooms=classrooms)