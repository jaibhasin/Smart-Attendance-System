# Smart Attendance System

A web-based attendance management platform built with Python and Flask. It allows administrators, teachers, students and parents to monitor attendance in real time.

## Features
- Role-based authentication for admins, teachers, students and parents
- Mark and track attendance per class and course
- Overview dashboards for administrators and teachers
- Simple interface built with Flask templates

## Setup
1. Clone the repository
   ```bash
   git clone https://github.com/yourusername/smart_attendance.git
   cd smart_attendance
   ```
2. Create a virtual environment and install dependencies
   ```bash
   python -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```
3. Run database migrations
   ```bash
   flask db upgrade
   ```
4. Launch the development server
   ```bash
   python app.py
   # or
   flask run
   ```

## Database
- SQLite is used for development (`myproject/data.sqlite`).
- Adjust the configuration in `myproject/__init__.py` if you wish to use another database engine.

## Folder Structure
- `myproject/` - main application package
- `migrations/` - Alembic migration scripts
- `static/` - CSS and image assets
- `templates/` - Jinja2 HTML templates

## License[MIT](LICENSE)
