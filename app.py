from flask import Flask, render_template, request, url_for, redirect
from datetime import date
import sqlite3

app = Flask(__name__)

@app.route('/')
def home():
    return render_template("index.html", date='{0:%A}, {0:%b}. {0:%d} ({0:%Y})'.format(date.today()))


# def get_db_connection(database):
#     # establishes a connection with the database and returns a connection object
#     conn = sqlite3.connect(database)
#     conn.row_factory = sqlite3.Row
#     return conn

# @app.route('/view_students')
# def view_students():
#     conn = get_db_connection('registrar.db')
#     query = "WITH stud (first_name, last_name, department, gpa) as " + \
#                 "(SELECT first_name, last_name, title, gpa " \
#                     "FROM student left outer join department " + \
#                         "ON student.department_id = department.id) " + \
#             "SELECT * FROM stud"
#     students = conn.execute(query).fetchall()
#     return render_template('view_students.html', students=students)

# @app.route('/add_student', methods=('GET', 'POST'))
# def add_student():
    
#     if request.method == 'GET':
#         return render_template('add_student.html', departmentNameNotFound=False)
    
#     if request.method == 'POST':
#         first_name = request.form['first_name']
#         last_name = request.form['last_name']
#         department = request.form['department']
#         gpa = request.form['gpa']

        
#         #check if department is valid
#         conn = get_db_connection('registrar.db')
        
#         query1 = "SELECT id FROM department WHERE title = \'" + str(department) + "\'"
#         idList = conn.execute(query1).fetchall()
#         if len(idList) == 1:
#             #insert the student into the db
#             departmentID = str(idList[0]['id'])
#             query = "INSERT INTO student (first_name, last_name, department_id, gpa) VALUES (\'"+ first_name + "\', \'" + last_name + "\', " + departmentID + ", " + gpa + ")"
#             conn.executescript(query)
#             conn.commit()
#             conn.close()
#             return redirect(url_for('added'))
#         else:
#             return render_template('add_student.html', departmentNameNotFound=True)
    

# @app.route('/view_departments')
# def view_dpartments():
#     conn = get_db_connection('registrar.db')
#     departments = conn.execute('SELECT * FROM department').fetchall()
#     return render_template('view_departments.html', departments=departments)


# @app.route('/add_dpartment', methods=('GET', 'POST'))
# def add_dpartment():

#     if request.method == 'GET':
#         return render_template('add_department.html')

#     if request.method == 'POST':
#         title = request.form['title']
#         faculty = request.form['faculty']

#         #insert entry
#         conn = get_db_connection('registrar.db')
#         query = "INSERT INTO department (title, faculty) VALUES (\'"+ title +"\', "+ faculty + ")"
#         conn.executescript(query)
#         conn.commit()
#         conn.close()

#         return redirect(url_for('added'))
 

# @app.route('/added')
# def added():
#     return render_template('added.html')
