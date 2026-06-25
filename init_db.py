import psycopg2

conn = psycopg2.connect(
    host="localhost",
    database="EmployeeDB",
    user="postgres",
    password="postgres@123",
    port="5432",
)
cur = conn.cursor()
conn.commit()
conn.close()

