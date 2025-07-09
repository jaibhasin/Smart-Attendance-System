from myproject.models import Student
from myproject import app, db

with app.app_context():

    s = Student('S1' , 'last_name' , 's1@thapar.edu' , 's1_123' , 'gururgam india' , '9899910122' , 'COE' )
    db.session.add(s)
    db.session.commit()


    # l = Student.query.all()
    # for i in l:
    #     print(i)