from flask import Flask, render_template, request, redirect
from flask_mysqldb import MySQL
import yaml


app = Flask(__name__)



# Configure db
db = yaml.safe_load(open('db.yaml'))
app.config['MYSQL_HOST'] = db['mysql_host']
app.config['MYSQL_USER'] = db['mysql_user']
app.config['MYSQL_PASSWORD'] = db['mysql_password']
app.config['MYSQL_DB'] = db['mysql_db']

mysql = MySQL(app)



@app.route('/insert', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Fetch form data
        studentDetails = request.form
        fname = studentDetails['fname']
        lname = studentDetails['lname']
        rollno = studentDetails['rollno']
        email = studentDetails['email']
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO student(fname, lname, rollno, email) VALUES(%s, %s, %s, %s)",(fname, lname, rollno, email))
        mysql.connection.commit()
        cur.close()
        return redirect("/")
    return render_template("index.html")

@app.route('/')
def students():
    cur = mysql.connection.cursor()
    resultValue = cur.execute("SELECT * FROM student")
    if resultValue > 0:
        studentDetails = cur.fetchall()
        return render_template('users.html',studentDetails=studentDetails)
    else:
        print("Empty Table")
    

    
@app.route('/delete/<int:id>', methods=['GET'])
def delete(id):
    cur = mysql.connection.cursor()
    cur.execute(f"DELETE FROM student WHERE id='{id}';")
    mysql.connection.commit()
    return redirect('/')


@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    if request.method == 'POST':
        studentDetails = request.form
        fname = studentDetails['fname']
        print(fname)
        lname = studentDetails['lname']
        rollno = studentDetails['rollno']
        email = studentDetails['email']
        print(f"UPDATE student SET fname = '{fname}', lname = '{lname}' , rollno = '{rollno}' , email = '{email}' where id='{id}';")
        cur = mysql.connection.cursor()
        cur.execute(f"UPDATE student SET fname = '{fname}', lname = '{lname}' , rollno = '{rollno}' , email = '{email}' WHERE id='{id}';")
        mysql.connection.commit()
        return redirect('/')
    else:
        cur = mysql.connection.cursor()
        resultValue = cur.execute(f"SELECT * FROM student where id='{id}';")
        if resultValue > 0:
            student = cur.fetchone()
            return render_template("update.html", student=student)

if __name__ == '__main__':
    app.run(debug=True)