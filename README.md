# 🎯 Face Recognition Attendance System

An intelligent **attendance management system** built with Python and OpenCV.  
It uses **face recognition** to mark attendance automatically — replacing manual sign-in sheets with smart automation.

---

## 🧠 Features

✅ **Admin Login System**  
- Secure admin authentication using CSV-based user storage.  
- Admin can add new users or change passwords.

✅ **Face Registration**  
- Capture and store face samples using a webcam.  
- Saves faces under `faces/<username>/` for easy retraining.

✅ **Model Training**  
- Trains a face recognition model on all registered users.

✅ **Take Attendance**  
- Recognizes faces live via webcam.  
- Automatically logs name, date, and time in `attendance.csv`.

✅ **View Attendance**  
- View and export attendance records directly from the dashboard.

---

## 🏗️ Project Structure

face_recognition_attendance/
│
├── admin_dashboard.py # Admin dashboard for all core features
├── login_gui.py # Login page for admin access
├── admin_utils.py # Handles authentication & password management
├── register_face.py # Captures and saves user face images
├── train_model.py # Trains the recognition model
├── take_attendance.py # Recognizes faces & records attendance
├── view_attendance.py # Displays attendance records
│
├── users.csv # Stores admin credentials & security answers
├── attendance.csv # Attendance logs (Name, Date, Time)
└── faces/ # Directory containing face samples


---

## ⚙️ Installation

### 1️⃣ Clone the Repository
```bash
git clone https://github.com/<amnsingh05>/<face-recognition-attendace-system>.git
cd face_recognition_attendance

2️⃣ Install Dependencies

Make sure Python 3.8+ is installed. Then, install the required libraries:

pip install opencv-python pandas numpy


💡 No need for dlib — this system is designed to work without it!

🚀 Usage Guide
🧑‍💻 Step 1: Run the Admin Login
python login_gui.py


Default credentials (you can change them later):

Username: admin

Password: 1234

🧍 Step 2: Register a New Face

Click “Register New Face”

Enter your name when prompted.

The system captures 30 face samples via webcam.

⚙️ Step 3: Train the Model

Click “Train Model” after registration to update the recognition model.

🕵️ Step 4: Take Attendance

Click “Take Attendance”

The camera will detect faces and automatically mark attendance in attendance.csv.

📋 Step 5: View Attendance

Click “View Attendance” to see all attendance logs.

🗂️ Example Attendance Record
Name	Date	Time
Aman	2025-11-02	09:42:10
Rahul	2025-11-02	09:45:12
Neha	2025-11-03	10:05:21

All attendance data is saved in attendance.csv automatically.

🧠 Technologies Used
Component	Technology
GUI	Tkinter
Face Detection	OpenCV (Haar Cascade Classifier)
Data Storage	CSV (Pandas)
Language	Python 3
📦 Dependencies

Install all dependencies using:

pip install -r requirements.txt


If you don’t have a requirements.txt yet, you can create one with:

opencv-python
pandas
numpy

🧑‍🏫 Example Command Line Usage

To quickly register a face without GUI:

python register_face.py


To take attendance directly:

python take_attendance.py


To view attendance:

python view_attendance.py

🧑‍💻 Author

Aman Singh
💼 💼 [LinkedIn](https://www.linkedin.com/in/amnsingh0)
📧 amansinghakr@gamil.com
