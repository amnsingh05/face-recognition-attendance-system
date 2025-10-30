from flask import Flask, render_template, request, redirect, url_for, session, flash
import csv
import bcrypt
import os
import cv2
from datetime import datetime
import webbrowser
import threading


app = Flask(__name__)
app.secret_key = 'your_secret_key'  # needed for session management

USERS_FILE = "users.csv"
ATTENDANCE_DIR = "teachers_attendance"

if not os.path.exists(ATTENDANCE_DIR):
    os.makedirs(ATTENDANCE_DIR)

def open_browser():
    webbrowser.open_new("http://127.0.0.1:5000")

if __name__ == "__main__":
    threading.Timer(1, open_browser).start()
    app.run(debug=False)

# ------------------ LOGIN ------------------
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        with open(USERS_FILE, "r") as file:
            reader = csv.DictReader(file)
            for row in reader:
                if row["username"] == username:
                    if bcrypt.checkpw(password.encode('utf-8'), row["password"].encode('utf-8')):
                        session['username'] = username
                        session['role'] = row["role"]
                        flash("Login successful!", "success")
                        return redirect(url_for('attendance_page'))
                    else:
                        flash("Incorrect password!", "danger")
                        return redirect(url_for('login'))
        flash("User not found!", "danger")
    return render_template('login.html')

# ------------------ REGISTER ------------------
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        question = request.form['security_question']
        answer = request.form['security_answer']
        role = "Teacher"  # default

        hashed_pw = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

        # check if username already exists
        with open(USERS_FILE, "r") as file:
            reader = csv.DictReader(file)
            for row in reader:
                if row["username"] == username:
                    flash("Username already exists!", "danger")
                    return redirect(url_for('register'))

        # append to users.csv
        with open(USERS_FILE, "a", newline="") as file:
            writer = csv.writer(file)
            writer.writerow([username, hashed_pw, role, question, answer.lower()])

        flash("Registration successful! Please login.", "success")
        return redirect(url_for('login'))

    return render_template('register.html')

# ------------------ ATTENDANCE PAGE ------------------
@app.route('/attendance')
def attendance_page():
    if 'username' not in session:
        flash("Please login first!", "warning")
        return redirect(url_for('login'))

    return render_template('attendance.html', username=session['username'])

# ------------------ ATTENDANCE MARKING ------------------
@app.route('/mark_attendance', methods=['POST'])
def mark_attendance():
    if 'username' not in session:
        return redirect(url_for('login'))

    username = session['username']
    today = datetime.now().strftime("%Y-%m-%d")
    file_path = os.path.join(ATTENDANCE_DIR, f"{username}_attendance.csv")

    cap = cv2.VideoCapture(0)
    ret, frame = cap.read()
    cap.release()

    if not ret:
        flash("Camera not working!", "danger")
        return redirect(url_for('attendance_page'))

    # (Placeholder) - Here you would call your face recognition logic
    # Simulate marking attendance
    if not os.path.exists(file_path):
        with open(file_path, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["Date", "Status"])

    with open(file_path, "a", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([today, "Present"])

    flash("Attendance marked successfully!", "success")
    return redirect(url_for('attendance_page'))

# ------------------ LOGOUT ------------------
@app.route('/logout')
def logout():
    session.clear()
    flash("Logged out successfully!", "info")
    return redirect(url_for('login'))

# ------------------ HOME REDIRECT ------------------
@app.route('/')
def home():
    return redirect(url_for('login'))

# ------------------ RUN ------------------
if __name__ == '__main__':
    app.run(debug=True)
