"""Smart Attendance System entry point."""
from myproject import app


def main() -> None:
    """Run the Flask development server."""
    app.run(debug=True)


if __name__ == '__main__':    main()
