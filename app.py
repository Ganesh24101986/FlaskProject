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


@app.route('/delete/<int:EmployeeId>', methods=['POST'])
def delete(EmployeeId):
    conn = db_conn()
    cur = conn.cursor()

    cur.execute('DELETE FROM "Employees" WHERE "EmployeeId" = %s', (EmployeeId,))

    conn.commit()
    cur.close()
    conn.close()

    return redirect(url_for('index'))

@app.route('/update/<int:EmployeeId>', methods=['GET', 'POST'])
def update(EmployeeId):
    conn = db_conn()
    cur = conn.cursor()

    if request.method == 'POST':
        name = request.form['name']
        department = request.form['department']
        salary = request.form['salary']

        cur.execute(
            'UPDATE "Employees" SET "Name" = %s, "Department" = %s, "Salary" = %s WHERE "EmployeeId" = %s',
            (name, department, salary, EmployeeId)
        )

        conn.commit()
        cur.close()
        conn.close()

        return redirect(url_for('index'))

    cur.execute('SELECT * FROM "Employees" WHERE "EmployeeId" = %s', (EmployeeId,))
    employee = cur.fetchone()
    cur.close()
    conn.close()

    return render_template('update.html', employee=employee)

@app.route('/')
def home():
    return "Hello, Flask!"

