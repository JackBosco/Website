from flask import Flask, render_template, request, url_for, redirect
import datetime
import time
import pyodbc
import requests
import sqlite3

app = Flask(__name__)

@app.route('/')
def home():
    updateDB(get_ip(), page='HOME')
    
    #updateDB(request.environ.get('HTTP_X_REAL_IP', request.remote_addr), page='HOME')
    #updateDB(request.remote_addr, page='HOME')
    return render_template("index.html", date='{0:%A}, {0:%b}. {0:%d} ({0:%Y})'.format(datetime.date.today()))

@app.route('/media')
def media():
    updateDB(get_ip(), page='MEDIA')
    return render_template("media.html")

@app.route('/resume')
def resume():
    updateDB(get_ip(), page='RESUME')
    return redirect(url_for('static', filename='images/resume.pdf'))

@app.route('/projects')
def projects():
    updateDB(get_ip(), page='PROJECTS')
    return render_template("projects.html")


def get_db_connection(database):
    # establishes a connection with the database and returns a connection object
    # Some other example server values are
    # server = 'localhost\sqlexpress' # for a named instance
    # server = 'myserver,port' # to specify an alternate port
    server = 'tcp:myserver.database.windows.net' 
    username = 'myusername' 
    password = 'mypassword'
    # ENCRYPT defaults to yes starting in ODBC Driver 18. It's good to always specify ENCRYPT=yes on the client side to avoid MITM attacks.
    cnxn = pyodbc.connect('DRIVER={ODBC Driver 18 for SQL Server};SERVER='+server+';DATABASE='+database+';ENCRYPT=yes;UID='+username+';PWD='+ password)
    cursor = cnxn.cursor()
    return cursor

def get_ip():
    resp = requests.get('https://api64.ipify.org?format=json').json()
    return resp["ip"]

def get_dataFromIP(ip_address):
    response = requests.get(f'https://ipapi.co/{ip_address}/json/').json()
    location_data = {
        "city": response.get("city"),
        "state": response.get("region"),
        "country": response.get("country_name"),
        "zipcode": response.get("postal"),
        "orgName": response.get("org")
    }
    return location_data

def updateDB(ip_address, page, method='GET'):
    clientData = get_dataFromIP(ip_address)
    updateTime = time.strftime('%Y-%m-%d %H:%M:%S')
    #conn = sqlite3.connect('server.db')
    conn = sqlite3.connect('temp.db')
    conn.row_factory = sqlite3.Row
    print(clientData["city"], clientData["state"], clientData["country"], clientData["zipcode"])
    try :
        conn.execute("""
                 INSERT INTO IP (IPv4Address) VALUES ('{ip}');
            """.format(ip=ip_address))
        conn.execute("""
                    INSERT INTO Client (IPv4, City, State, Country, zip) VALUES ('{ip}', '{city}', '{state}', '{country}', {zip});
            """.format(ip=ip_address, city=clientData["city"], state=clientData["state"], country=clientData["country"],
                zip=clientData["zipcode"]))
        conn.execute("""
                    INSERT INTO Organization (OrgName) VALUES ('{orgName}');
            """.format(orgName=clientData["orgName"]))
        conn.execute("""
                 INSERT INTO Services (OrgName, IPv4) VALUES ('{orgName}', '{ip}');
            """.format(ip=ip_address, orgName=clientData["orgName"]))
    except :
        print("ip revisit")
    conn.execute("""
                 INSERT INTO Request (IPv4, RenderPage, Method, TimeOfRequest) VALUES ('{ip}', '{p}', '{req}', '{t}');
    """.format(ip=ip_address, p=page, req=method, t=updateTime))
    conn.commit()
    conn.close()
    

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
