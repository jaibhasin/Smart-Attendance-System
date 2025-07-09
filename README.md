# Smart Attendance System

A web-based attendance management system for schools/universities, built with Python and Flask.

## Features
- Admin, Teacher, Student, and Parent logins
- Attendance marking and tracking
- Classroom and course management
- User-friendly web interface

## Setup
1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/smart_attendance.git
   cd smart_attendance
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run the application:
   ```bash
   python app.py
   ```

## Database
- Uses SQLite by default (see `myproject/data.sqlite`).
- For production, configure your preferred database in `myproject/models.py` and `database_queries.py`.

## Folder Structure
- `myproject/` - Main application code
- `migrations/` - Database migrations (Alembic)
- `static/` - Static assets (CSS, images)
- `templates/` - HTML templates

## License
[MIT](LICENSE) 