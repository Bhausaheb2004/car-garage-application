from flask import Flask, render_template, request, redirect, session
import mysql.connector

app = Flask(__name__)
app.secret_key = "secret123"

# ---------------- DB CONNECTION ----------------
def get_db():
    return mysql.connector.connect(
        host="localhost",
        user="root",          # change if needed
        password="1234",          # your MySQL password
        database="car_garage"
    )

# ---------------- CREATE TABLES ----------------
def create_tables():
    conn = get_db()
    cur = conn.cursor()

    # USERS TABLE
    cur.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INT AUTO_INCREMENT PRIMARY KEY,
        name VARCHAR(100),
        email VARCHAR(100) UNIQUE,
        password VARCHAR(100)
    )
    """)

    # BOOKINGS TABLE
    cur.execute("""
    CREATE TABLE IF NOT EXISTS bookings (
        id INT AUTO_INCREMENT PRIMARY KEY,
        user_id INT,
        name VARCHAR(100),
        phone VARCHAR(20),
        car VARCHAR(100),
        service VARCHAR(100),
        date VARCHAR(20)
    )
    """)

    conn.commit()
    conn.close()

create_tables()

# ---------------- HOME ----------------
@app.route('/')
def home():
    if 'user_id' not in session:
        return redirect('/login')
    return render_template('index.html')

# ---------------- REGISTER ----------------
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']

        conn = get_db()
        cur = conn.cursor()

        try:
            cur.execute(
                "INSERT INTO users (name, email, password) VALUES (%s, %s, %s)",
                (name, email, password)
            )
            conn.commit()
        except:
            conn.close()
            return "Email already exists!"

        conn.close()
        return redirect('/login')

    return render_template('register.html')

# ---------------- LOGIN ----------------
@app.route('/login', methods=['GET', 'POST'])
def login():
    if 'user_id' in session:
        return redirect('/booking')

    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        conn = get_db()
        cur = conn.cursor(dictionary=True)

        cur.execute(
            "SELECT * FROM users WHERE email=%s AND password=%s",
            (email, password)
        )
        user = cur.fetchone()
        conn.close()

        if user:
            session['user_id'] = user['id']
            session['user_name'] = user['name']
            return redirect('/booking')
        else:
            return "Invalid Email or Password"

    return render_template('login.html')

# ---------------- LOGOUT ----------------
@app.route('/logout')
def logout():
    session.clear()
    return redirect('/login')

# ---------------- BOOKING ----------------
@app.route('/booking', methods=['GET', 'POST'])
def booking():
    if 'user_id' not in session:
        return redirect('/login')

    if request.method == 'POST':
        name = request.form['name']
        phone = request.form['phone']
        car = request.form['car']
        service = request.form['service']
        date = request.form['date']
        user_id = session['user_id']

        conn = get_db()
        cur = conn.cursor()

        cur.execute("""
        INSERT INTO bookings (user_id, name, phone, car, service, date)
        VALUES (%s, %s, %s, %s, %s, %s)
        """, (user_id, name, phone, car, service, date))

        conn.commit()
        conn.close()

        return redirect('/booking')

    return render_template('booking.html')

# ---------------- RUN ----------------
if __name__ == "__main__":
    app.run(debug=True)
