from flask import Flask, redirect, url_for, render_template, request, session, jsonify
from flask_mysqldb import MySQL
import MySQLdb.cursors
import re
from datetime import timedelta
from flask_cors import CORS
from flask_mail import Mail, Message

app = Flask(__name__)
# Change this to your secret key (can be anything, it's for extra protection)
app.secret_key = "secret key"
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=10)
CORS(app)

# Enter your database connection details below
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'root'
app.config['MYSQL_DB'] = 'project'

# Email Settings
# app.config['MAIL_SERVER'] = 'localhost'
# app.config['MAIL_PORT'] = 587
# app.config['MAIL_TLS'] = False
# app.config['MAIL_SSL'] = True
# app.config['MAIL_USERNAME'] = 'alex.ruoff.fitness@gmail.com'
# app.config['MAIL_DEFAULT_SENDER'] = 'alex.ruoff.fitness@gmail.com'
# app.config['MAIL_PASSWORD'] = '@Sandwich!'

app.config.update(dict(
    DEBUG=True,
    MAIL_SERVER='smtp.gmail.com',
    MAIL_PORT=587,
    MAIL_USE_TLS=True,
    MAIL_USE_SSL=False,
    MAIL_USERNAME='alex.ruoff.fitness@gmail.com',
    MAIL_DEFAULT_SENDER='alex.ruoff.fitness@gmail.com',
    MAIL_PASSWORD='@Sandwich!',
))

mail = Mail(app)

# Intialize MySQLa
mysql = MySQL(app)


@app.route('/')
def about():
    return render_template("/about.html")


@app.route("/login")
def home():
    return render_template("login.html")


@app.route("/blog")
def blog():
    return render_template("blog.html")


@app.route("/reminder", methods=['GET', 'POST'])
def reminder():
    msg = ' '

    if request.method == 'POST' and 'name' in request.form and 'email' in request.form:
        name = request.form['name']
        email = request.form['email']

        # Check if Email exists using MySQL
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM REMINDER WHERE reminder_email = %s', (email,))
        reminderdata = cursor.fetchone()

        # If account exists show error and validation checks
        if reminderdata:
            msg = 'You are already subscribed'
            return render_template('reminder.html', msg=msg)

        elif not re.match(r'[A-Za-z]+', name):
            msg = 'Name must contain only characters!'
            return render_template('reminder.html', msg=msg)

        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            msg = 'Invalid email address!'
            return render_template('reminder.html', msg=msg)

        else:
            # Account doesnt exists and the form data is valid, now insert new account into accounts table
            cursor.execute(
                'INSERT INTO REMINDER (reminder_name, reminder_email) VALUES ( %s, %s)',
                (name, email,))
            mysql.connection.commit()

            emsg = Message("Welcome to Alex's Ruoffs Reminders", recipients=[email])

            emsg.body = 'Hello, ' + name + ' Thank you for subscribing for your appiontment reminders.'

            mail.send(emsg)

            msg = 'You have successfully Subscribed!'
            return render_template('reminder.html', msg=msg)

    return render_template("reminder.html")


# Display Calendar
@app.route('/calendar')
def calendar():
    return render_template('calendar_events.html')


# Display Cardio Workouts
@app.route("/Cardio")
def cardio():
    return render_template("cardio.html")


# Display Abs Workout
@app.route("/Abs")
def abs():
    return render_template("abs.html")


# Display Arms Workout
@app.route("/Arms")
def arms():
    return render_template("arms.html")


# Display Compound Workout
@app.route("/Compound")
def compound():
    return render_template("compound.html")


# Display Legs Workout
@app.route("/Legs")
def legs():
    return render_template("legs.html")


# Display Shoulders Workout
@app.route("/Shoulders")
def shoulders():
    return render_template("shoulders.html")


# Client Sign - Sign up clients, Hyperlink to go back to Homepage/Calendar
@app.route("/signup", methods=["POST", "GET"])
def signup():
    msg = ''

    if request.method == 'POST' and 'firstname' in request.form and 'lastname' in request.form and 'middlename' in request.form and 'email' in request.form and 'phonenumber' in request.form and 'birthdate' in request.form and 'gender' in request.form and 'height' in request.form and 'weight' in request.form and 'background' in request.form:

        firstname = request.form['firstname']
        lastname = request.form['lastname']
        middlename = request.form['middlename']
        email = request.form['email']
        phonenumber = request.form['phonenumber']
        birthdate = request.form['birthdate']
        gender = request.form['gender']
        height = request.form['height']
        weight = request.form['weight']
        background = request.form['background']

        # Check if account exists using MySQL
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM CLIENT WHERE client_email = %s', (email,))
        clientdata = cursor.fetchone()

        # If account exists show error and validation checks
        if clientdata:
            msg = 'Client already exists!'
            return render_template('signupPage.html', msg=msg)

        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            msg = 'Invalid email address!'
            return render_template('signupPage.html', msg=msg)

        elif not re.match(r'[A-Za-z]+', firstname):
            msg = 'First name must contain only characters!'
            return render_template('signupPage.html', msg=msg)

        elif not re.match(r'[A-Za-z]+', lastname):
            msg = 'Last name must contain only characters!'
            return render_template('signupPage.html', msg=msg)

        elif not re.match(r'[0-9]+', phonenumber):
            msg = 'Phone number must contain only numbers!'
            return render_template('signupPage.html', msg=msg)

        elif not firstname or not lastname or not email:
            msg = "Please fill out the client's information"
            return render_template('signupPage.html', msg=msg)

        else:
            # Account doesnt exists and the form data is valid, now insert new account into accounts table
            cursor.execute(
                'INSERT INTO CLIENT (client_firstname, client_lastname, client_middlename, client_email, client_phonenumber, client_birthdate, client_gender, client_height, client_weight, client_background) VALUES ( %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)',
                (firstname, lastname, middlename, email, phonenumber, birthdate, gender, height, weight, background,))
            mysql.connection.commit()
            msg = 'You have successfully registered: ' + firstname + ' ' + lastname
            return render_template('signupPage.html', msg=msg)

    elif request.method == 'POST':
        # Form is empty... (no POST data)
        msg = 'Please fill out the form!'

    # Show registration form with message (if any)
    return render_template('signupPage.html', msg=msg)
    # Redirect to display page with message and than from display page go to home page


# User_Registration - directed from login page, leads back to login page
@app.route("/userregistration", methods=['GET', 'POST'])
def userregistration():
    msg = ''
    if request.method == 'POST' and 'firstname' in request.form and 'lastname' in request.form and 'middlename' in request.form and 'email' in request.form and 'username' in request.form and 'password' in request.form and 'birthdate' in request.form:

        # Create variables for easy access
        firstname = request.form['firstname']
        lastname = request.form['lastname']
        middlename = request.form['middlename']
        email = request.form['email']
        username = request.form['username']
        password = request.form['password']
        birthdate = request.form['birthdate']

        # Check if account exists using MySQL
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM USER WHERE user_username = %s', (username,))
        account = cursor.fetchone()

        # If account exists show error and validation checks
        if account:
            msg = 'Account already exists!'
            return render_template('userregistration.html', msg=msg)

        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            msg = 'Invalid email address!'
            return render_template('userregistration.html', msg=msg)

        elif not re.match(r'[A-Za-z0-9]+', username):
            msg = 'Username must contain only characters and numbers!'
            return render_template('userregistration.html', msg=msg)

        elif not username or not password or not email:
            msg = 'Please fill out the form!'
            return render_template('userregistration.html', msg=msg)

        else:
            # Account doesnt exists and the form data is valid, now insert new account into accounts table
            cursor.execute(
                'INSERT INTO USER (user_firstname, user_lastname, user_middlename, user_username, user_password, user_email, user_birthdate) VALUES ( %s, %s, %s, %s, %s, %s, %s)',
                (firstname, lastname, middlename, username, password, email, birthdate,))
            mysql.connection.commit()
            msg = 'You have successfully registered!'
            return render_template('login.html', msg=msg)

    elif request.method == 'POST':
        # Form is empty... (no POST data)
        msg = 'Please fill out the form!'

    # Show registration form with message (if any)
    return render_template('userregistration.html', msg=msg)
    # Redirect to display page with message and than from display page go to home page


# login- First page you see, Either login, button to register a user
@app.route('/login', methods=['GET', 'POST'])
def login():
    # Output message if something goes wrong...
    msg = ''

    # Check if "username" and "password" POST requests exist (user submitted form)
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        # Create variables for easy access
        username = request.form['username']
        password = request.form['password']

        # Check if account exists using MySQL
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM USER WHERE user_username = %s AND user_password = %s', (username, password,))
        # Fetch one record and return result
        account = cursor.fetchone()

        # If account exists in accounts table in out database
        if account:
            # Create session data, we can access this data in other routes
            session['loggedin'] = True
            session['id'] = account['user_id']
            session['username'] = account['user_username']

            # Redirect to home page/ Calendar
            return render_template('calendar_events.html', un=username)

        else:
            # Account doesnt exist or username/password incorrect
            msg = 'Incorrect username/password!'

    # Show the login form with message (if any)
    return render_template('login.html', msg=msg)


# schedule appoitment - adds an event into the event database
@app.route('/scheduleappointment', methods=['GET', 'POST'])
def scheduleappointment():
    # Output message if something goes wrong...
    msg = ''

    if request.method == 'POST' and 'title' in request.form and 'url' in request.form and 'classname' in request.form and 'startdate' in request.form and 'enddate' in request.form:
        # Create variables for easy access
        title = request.form['title']
        url = request.form['url']
        classname = request.form['classname']
        startdate = request.form['startdate']
        enddate = request.form['enddate']

        # Check if account exists using MySQL - checks by title might change to startdate later******
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM event WHERE title = %s AND url = %s', (title, url))
        event = cursor.fetchone()

        # If event already exists show error
        if event:
            msg = 'event already exists!'
            return render_template('scheduleappointment.html', msg=msg)

        else:
            # Account doesnt exists and the form data is valid, now insert new account into accounts table
            cursor.execute(
                'INSERT INTO event (title, url, class, start_date, end_date) VALUES ( %s, %s, %s, %s, %s)',
                (title, url, classname, startdate, enddate,))
            mysql.connection.commit()
            msg = 'You have successfully added an event!'
            return render_template('calendar_events.html')

    elif request.method == 'POST':
        # Form is filled out incorrectly (no POST data)
        msg = 'Please fill out the event properly!'

    # Show registration form with message (if any)
    return render_template('scheduleappointment.html', msg=msg)
    # Redirect to display page with message and than from display page go to home page


# Calendar
@app.route('/calendar-events')
def calendar_events():
    cursor = None
    try:
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute(
            "SELECT id, title, url, class, UNIX_TIMESTAMP(start_date)*1000 as start, UNIX_TIMESTAMP(end_date)*1000 as end FROM project.event")
        rows = cursor.fetchall()
        resp = jsonify({'success': 1, 'result': rows})
        resp.status_code = 200
        return resp
    except Exception as e:
        print(e)
    finally:
        cursor.close()


# Delete Client
@app.route("/manageclient", methods=['GET', 'POST', 'delete'])
def manageclient():
    msg = ''

    cursor = mysql.connection.cursor()

    if request.method == 'POST':
        # cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        client_id = request.form['client_id']
        cursor.execute("DELETE FROM project.client where client_id = %s", (client_id,))
        mysql.connection.commit()

        cursor.execute("select * from client")
        data = cursor.fetchall()  # data from database
        return render_template("manageclient.html", value=data)

    cursor.execute("select * from client")
    data = cursor.fetchall()  # data from database
    return render_template("manageclient.html", value=data)


@app.route("/contact", methods=['GET', 'POST'])
def contact():
    # Output message if something goes wrong...
    msg = ''

    if request.method == 'POST' and 'firstname' in request.form and 'lastname' in request.form and 'phone_number' in request.form and 'email' in request.form and 'subject' in request.form:

        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)

        firstname = request.form['firstname']
        lastname = request.form['lastname']
        phonenumber = request.form['phone_number']
        email = request.form['email']
        subject = request.form['subject']

        # If account exists show error and validation checks

        if not re.match(r'[A-Za-z]+', firstname):
            msg = 'First name must contain only characters!'
            return render_template('contact.html', msg=msg)

        elif not re.match(r'[A-Za-z]+', lastname):
            msg = 'Last name must contain only characters!'
            return render_template('contact.html', msg=msg)

        elif not re.match(r'[0-9]+', phonenumber):
            msg = 'Phone number must contain only numbers!'
            return render_template('contact.html', msg=msg)

        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            msg = 'Invalid email address!'
            return render_template('contact.html', msg=msg)

        else:
            # Account doesnt exists and the form data is valid, now insert new account into accounts table
            cursor.execute(
                'INSERT INTO contact (contact_firstname, contact_lastname, contact_phonenumber, contact_email, contact_subject) VALUES ( %s, %s, %s, %s, %s)',
                (firstname, lastname, phonenumber, email, subject,))
            mysql.connection.commit()
            msg = 'You have successfully sent your message to Alex: '
            return render_template('contact.html', msg=msg)

    # Show the contact form with message (if any)
    return render_template('contact.html', msg=msg)


@app.route('/inquiry', methods=['GET', 'POST', 'delete'])
def inquiry():
    cursor = mysql.connection.cursor()

    if request.method == 'POST':
        contact_id = request.form['contact_id']
        cursor.execute("DELETE FROM project.contact where contact_id = %s", (contact_id,))
        mysql.connection.commit()

        cursor.execute("select * from contact")
        data = cursor.fetchall()  # data from database
        return render_template("inquiry.html", value=data)

    cursor.execute("select * from contact")
    data = cursor.fetchall()  # data from database
    return render_template('/inquiry.html', value=data)


@app.route('/reminderSignUp', methods=['GET', 'POST', 'delete'])
def reminderSignUp():
    cursor = mysql.connection.cursor()

    if request.method == 'POST':
        contact_id = request.form['reminder_id']
        cursor.execute("DELETE FROM project.reminder where reminder_id = %s", (contact_id,))
        mysql.connection.commit()

        cursor.execute("select * from reminder")
        data = cursor.fetchall()  # data from database
        return render_template("reminderSignUp.html", value=data)

    cursor.execute("select * from reminder")
    data = cursor.fetchall()  # data from database
    return render_template('/reminderSignUp.html', value=data)


# @app.route("/removeclient", methods = ['delete'])
# def removeclient():
#     cursor = mysql.connection.cursor()
#
#     if request.method == 'delete':
#     #     client_id = request.form['client_id']
#         cursor.execute("DELETE FROM project.client where client_id = 3", ())
#
#     #     data = cursor.fetchall()  # data from database
#     #     return render_template("manageclient.html", value=data)
#     #
#     cursor.execute("select * from client")
#     data = cursor.fetchall()  # data from database
#     return render_template("manageclient.html", value=data)

# Modify/Update Client page
@app.route("/modifyclient", methods=['GET', 'POST'])
def modifyclient():
    cursor = mysql.connection.cursor()

    if request.method == 'POST' and 'firstname' in request.form and 'lastname' in request.form and 'middlename' in request.form and 'email' in request.form and 'phonenumber' in request.form and 'birthdate' in request.form and 'gender' in request.form and 'height' in request.form and 'weight' in request.form and 'background' in request.form:
        firstname = request.form.get('firstname')
        lastname = request.form.get('lastname')
        middlename = request.form.get('middlename')
        email = request.form.get('email')
        phonenumber = request.form.get('phonenumber')
        birthdate = request.form.get('birthdate')
        gender = request.form.get('gender')
        height = request.form.get('height')
        weight = request.form.get('weight')
        background = request.form.get('background')
        client_id = request.form.get('client_id')

        # update first name
        if firstname != '':
            cursor.execute('Update client set client_firstname=%s where client_id = %s', (firstname, client_id,))
            mysql.connection.commit()

        if middlename != '':
            cursor.execute('Update client set client_middlename=%s where client_id = %s', (middlename, client_id,))
            mysql.connection.commit()

        if lastname != '':
            cursor.execute('Update client set client_lastname=%s where client_id = %s', (lastname, client_id,))
            mysql.connection.commit()

        if email != '':
            cursor.execute('Update client set client_email=%s where client_id = %s', (email, client_id,))
            mysql.connection.commit()

        if phonenumber != '':
            cursor.execute('Update client set client_phonenumber=%s where client_id = %s', (phonenumber, client_id,))
            mysql.connection.commit()

        if birthdate != '':
            cursor.execute('Update client set client_birthdate=%s where client_id = %s', (birthdate, client_id,))
            mysql.connection.commit()

        if gender != '':
            cursor.execute('Update client set client_gender=%s where client_id = %s', (gender, client_id,))
            mysql.connection.commit()

        if height != '':
            cursor.execute('Update client set client_height=%s where client_id = %s', (height, client_id,))
            mysql.connection.commit()

        if weight != '':
            cursor.execute('Update client set client_weight=%s where client_id = %s', (weight, client_id,))
            mysql.connection.commit()

        if background != '':
            cursor.execute('Update client set client_background=%s where client_id = %s', (background, client_id,))
            mysql.connection.commit()

        # cursor.execute(
        #     'Update client set client_firstname=%s, client_lastname=%s, client_middlename=%s, client_email=%s, client_phonenumber=%s, client_birthdate=%s, client_gender=%s, client_height=%s, client_weight=%s, client_background=%s  where client_id = %s',
        #     (firstname, lastname, middlename, email, phonenumber, birthdate, gender, height, weight, background,
        #      client_id,))
        # mysql.connection.commit()

        # msg = 'You have successfully Updated a register!'

    cursor.execute("select * from client")
    data = cursor.fetchall()  # data from database
    return render_template('modifyclient.html', value=data)


# Cancel Appointment
@app.route("/cancelappointment", methods=['GET', 'POST'])
def cancelappointment():
    cursor = mysql.connection.cursor()

    if request.method == 'POST':
        # cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        event_id = request.form['id']
        cursor.execute("DELETE FROM project.event where id = %s", (event_id,))
        mysql.connection.commit()

        cursor.execute("select * from event")
        data = cursor.fetchall()  # data from database
        return render_template("cancelappointment.html", value=data)

    cursor.execute("select * from event")
    data = cursor.fetchall()  # data from database
    return render_template("cancelappointment.html", value=data)


# Reschedule Appointment
@app.route("/rescheduleappointment", methods=['GET', 'POST'])
def rescheduleappointment():
    cursor = mysql.connection.cursor()

    if request.method == 'POST' and 'title' in request.form and 'url' in request.form and 'classname' in request.form and 'startdate' in request.form and 'enddate' in request.form:
        # Create variables for easy access
        title = request.form['title']
        url = request.form['url']
        classname = request.form['classname']
        startdate = request.form['startdate']
        enddate = request.form['enddate']
        event_id = request.form.get('id')

        if title != '':
            cursor.execute('Update event set title=%s where id = %s', (title, event_id,))
            mysql.connection.commit()

        if url != '':
            cursor.execute('Update event set url =%s where id = %s', (url, event_id,))
            mysql.connection.commit()

        if classname != '':
            cursor.execute('Update event set class =%s where id = %s', (classname, event_id,))
            mysql.connection.commit()

        if startdate != '':
            cursor.execute('Update event set start_date =%s where id = %s', (startdate, event_id,))
            mysql.connection.commit()

        if enddate != '':
            cursor.execute('Update event set end_date =%s where id = %s', (enddate, event_id,))
            mysql.connection.commit()

    cursor.execute("select * from event")
    data = cursor.fetchall()  # data from database
    return render_template("rescheduleappointment.html", value=data)


if __name__ == "__main__":
    app.run(debug=True)
