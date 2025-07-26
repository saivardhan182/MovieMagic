from flask import Flask, render_template, request, redirect, flash, url_for, session
import sqlite3, os, smtplib
from email.message import EmailMessage
from dotenv import load_dotenv
from aws_app import store_in_dynamodb, send_sns_notification

# Load environment variables
load_dotenv()
EMAIL_USER = os.getenv('EMAIL_ADDRESS')
EMAIL_PASS = os.getenv('EMAIL_PASSWORD')

app = Flask(__name__)
app.secret_key = 'your_secret_key'
DB_PATH = 'users.db'

# Initialize users table
def init_db():
    if not os.path.exists(DB_PATH):
        with sqlite3.connect(DB_PATH) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                CREATE TABLE users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    fullname TEXT NOT NULL,
                    email TEXT NOT NULL UNIQUE,
                    password TEXT NOT NULL
                )
            ''')
            conn.commit()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        fullname = request.form['fullname']
        email = request.form['email']
        password = request.form['password']

        with sqlite3.connect(DB_PATH) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM users WHERE email = ?", (email,))
            if cursor.fetchone():
                flash("Email already exists!", "error")
                return redirect(url_for('signup'))

            cursor.execute("INSERT INTO users (fullname, email, password) VALUES (?, ?, ?)",
                           (fullname, email, password))
            conn.commit()
            flash("Account created successfully!", "success")
            return redirect(url_for('login'))
    return render_template('signup.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        with sqlite3.connect(DB_PATH) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM users WHERE email = ? AND password = ?", (email, password))
            user = cursor.fetchone()

            if user:
                session['fullname'] = user[1]
                return redirect(url_for('dashboard'))
            else:
                flash("Invalid credentials!", "error")
                return redirect(url_for('login'))
    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    if 'fullname' not in session:
        flash("Please log in.", "error")
        return redirect(url_for('login'))
    return render_template('dashboard.html')

@app.route('/results')
def results():
    city = request.args.get('city')
    language = request.args.get('language')

    conn = sqlite3.connect('movies.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM movies WHERE LOWER(city)=LOWER(?) AND LOWER(language)=LOWER(?)", (city, language))
    movies = cursor.fetchall()
    conn.close()

    return render_template("results.html", movies=movies)

@app.route('/book/<movie>', methods=['GET', 'POST'])
def book(movie):
    if request.method == 'POST':
        session['booking'] = request.form.to_dict()
        session['booking']['movie'] = movie
        return redirect(url_for('select_seats'))
    return render_template('booking.html', movie=movie)

@app.route('/select_seats', methods=['GET', 'POST'])
def select_seats():
    if request.method == 'POST':
        if 'booking' not in session:
            flash("Booking session expired.", "error")
            return redirect(url_for('dashboard'))

        seats = request.form.get('seats')
        if not seats:
            flash("Please select at least one seat.", "error")
            return redirect(url_for('select_seats'))

        booking = session['booking']
        for key in ['name', 'email', 'phone', 'movie', 'date', 'time', 'seats']:
            booking[key] = request.form.get(key)
        session['booking'] = booking

        print("✅ Full booking session data:", session['booking'])
        return redirect(url_for('payment'))

    booking_data = session.get('booking')
    if not booking_data:
        flash("Session expired. Please try again.", "error")
        return redirect(url_for('dashboard'))
    return render_template('select_seats.html', booking_data=booking_data)

@app.route('/payment', methods=['GET', 'POST'])
def payment():
    if 'booking' not in session:
        flash("Booking session expired. Please start again.", "error")
        return redirect(url_for('dashboard'))

    if request.method == 'POST':
        booking = session['booking']
        booking['payment'] = request.form['payment']
        booking['amount'] = request.form['amount']
        session['booking'] = booking
        return redirect(url_for('confirm_booking'))

    booking = session['booking']
    seat_list = booking['seats'].split(',') if booking['seats'] else []
    ticket_price = 125
    total_amount = len(seat_list) * ticket_price
    booking['amount'] = total_amount
    session['booking'] = booking

    return render_template('payment.html', booking=booking)

@app.route('/confirm')
def confirm_booking():
    data = session.get('booking')
    if not data:
        flash("Booking session expired.", "error")
        return redirect(url_for('dashboard'))

    print("📦 Booking data at /confirm:", data)
    print("✅ Sending email to:", data['email'])

    send_email(data)
    store_in_dynamodb(data)
    send_sns_notification(data)

    return render_template('ticket.html', details=data, movie=data['movie'])

def send_email(data):
    msg = EmailMessage()
    msg['Subject'] = '🎟️ Movie Ticket Confirmation'
    msg['From'] = EMAIL_USER
    msg['To'] = data['email']

    msg.set_content(f"""
Hi {data['name']},

Your movie ticket is confirmed! 🎉

🎟️ Ticket Details
--------------------------
🎬 Movie   : {data['movie']}
📅 Date    : {data['date']}
⏰ Time    : {data['time']}
💺 Seats   : {data['seats']}
💳 Payment : {data['payment']}
💰 Amount  : ₹{data['amount']}

Thank you for booking with MovieMagic! 🍿
Enjoy your show!

- MovieMagic Team
    """)

    try:
        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls()
            server.login(EMAIL_USER, EMAIL_PASS)
            server.send_message(msg)
    except Exception as e:
        print("❌ Email sending failed:", e)

@app.route('/logout')
def logout():
    session.clear()
    flash("Logged out.", "info")
    return redirect(url_for('index'))

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
