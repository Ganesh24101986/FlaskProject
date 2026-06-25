import psycopg2
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

if __name__ == '__main__':
    app.run(debug=True)

def db_conn():
    conn = psycopg2.connect(
        host="localhost",
        database="EmployeeDB",
        user="postgres",
        password="postgres@123",
        port="5432",
    )
    return conn

@app.route("/index")
def index():
    conn = db_conn()
    cur = conn.cursor()
    cur.execute('SELECT * FROM "Employees";')
    employees = cur.fetchall()
    conn.commit()
    cur.close()
    conn.close()
    return render_template("index.html", employees=employees) 

@app.route('/create', methods=['GET', 'POST'])
def create():
    if request.method == 'POST':
        name = request.form['name']
        department = request.form['department']
        salary = request.form['salary']

        conn = db_conn()
        cur = conn.cursor()

        cur.execute(
            'INSERT INTO "Employees" ("Name", "Department", "Salary") VALUES (%s, %s, %s)',
            (name, department, salary)
        )

        conn.commit()
        cur.close()
        conn.close()

        return redirect(url_for('index'))

    return render_template('create.html')

@app.route('/')
def home():
    return "Hello, Flask!"

