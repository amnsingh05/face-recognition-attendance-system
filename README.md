# 🎯 Face Recognition Attendance System

An intelligent **attendance management system** built with Python and OpenCV.  
It uses **face recognition**, **liveness detection**, and **geofencing (campus-boundary validation)** to mark attendance securely and automatically.

---

## 🧠 Features

✅ **Admin Login System**  
- Secure admin authentication using CSV-based user storage.  
- Admin can add new users, change passwords, and reset credentials.  

✅ **Face Registration**  
- Capture and store multiple face samples using a webcam.  
- Saves faces under `faces/<username>/` for model retraining.  

✅ **Model Training**  
- Trains an OpenCV LBPH model on all registered user faces.  
- Stores trained data in `trainer/trainer.yml`.  

✅ **Liveness Detection (Anti-Spoofing)**  
- Uses **CVZone FaceMesh** to detect blinking and eye movement.  
- Attendance is only marked when a **real, live face** is detected (prevents cheating with photos or videos).  
- Ensures “live verification” before attendance is saved.  

✅ **Geo-Fenced Attendance (Campus Boundary Check)**  
- Attendance can only be marked **within the authorized campus area**.  
- Uses geographic location (latitude, longitude) validation to confirm user is on-site.  
- Prevents attendance marking from remote or off-campus locations.  

✅ **Take Attendance**  
- Recognizes faces in real time using webcam feed.  
- Marks attendance only if both **liveness** and **location checks** pass.  
- Stores results in `attendance/attendance_YYYY-MM-DD.csv`.

✅ **View Attendance**  
- View daily or historical attendance directly from the admin dashboard.  
- Export data to CSV/Excel.

---

## 🏗️ Project Structure

```
face_recognition_attendance/
│
├── admin_dashboard.py        # Admin dashboard for all core features
├── login_gui.py              # Login page for admin access
├── admin_utils.py            # Handles authentication & password management
├── register_face.py          # Captures and saves user face images
├── train_model.py            # Trains the face recognition model
├── take_attendance.py        # Recognizes faces & records attendance
├── view_attendance.py        # Displays attendance records
├── liveness_check.py         # Detects blinking / liveness (anti-spoofing)
├── location_utils.py         # Verifies geographic boundaries (campus check)
│
├── users.csv                 # Stores admin credentials
├── attendance/               # Folder containing daily attendance CSVs
└── faces/                    # Directory with face samples
```

---

## ⚙️ Installation

### 1️⃣ Clone the Repository
```bash
git clone https://github.com/amnsingh05/face-recognition-attendance-system.git
cd face_recognition_attendance
```

### 2️⃣ Install Dependencies
Make sure Python 3.8+ is installed. Then run:
```bash
pip install opencv-python pandas numpy cvzone geopy
```

💡 *No need for dlib — this system is designed to work without it!*

---

## 🚀 Usage Guide

### 🧑‍💻 Step 1: Run the Admin Login
```bash
python login_gui.py
```
Default credentials:
```
Username: admin
Password: 1234
```

### 🧍 Step 2: Register Faces
- Click **“Register New Face”** and enter a username.  
- The system captures 30 face samples automatically.

### ⚙️ Step 3: Train the Model
Click **“Train Model”** to update the trained dataset.

### 🕵️ Step 4: Take Attendance
- Click **“Take Attendance”**.  
- System checks:
  1. Live face detection (blink/eye movement).  
  2. Geo-location inside campus.  
  3. Face match confidence.  
- Only after passing all checks, attendance is recorded.

### 📋 Step 5: View Attendance
Click **“View Attendance”** to view or export all attendance logs.

---

## 🗺️ Example Geo-Fencing Configuration
Campus boundary (example):
```python
CAMPUS_CENTER = (28.6139, 77.2090)  # Example: Delhi coordinates
RADIUS_METERS = 100  # Attendance allowed within 100 meters
```

If the device location is outside this radius, attendance will not be marked.

---

## 🧠 Technologies Used

| Component | Technology |
|------------|-------------|
| GUI | Tkinter |
| Face Detection | OpenCV (Haar Cascade + LBPH) |
| Liveness Detection | CVZone (FaceMesh Eye Blink) |
| Geo-Fencing | Geopy (Distance Validation) |
| Data Storage | CSV (via Pandas) |
| Language | Python 3 |

---

## 📦 Dependencies
```
opencv-python
pandas
numpy
cvzone
geopy
```

Install all dependencies with:
```bash
pip install -r requirements.txt
```

---

## 🧑‍💻 Authors

**Aaryan Sharma**  
💼 [LinkedIn](https://www.linkedin.com/in/aaryan-sharma-a341a732b/)  
📧 aaryansharma90898@gmail.com  

**Aksh Jain**  
💼 [LinkedIn](https://www.linkedin.com/in/aksh-jain-58a705203/)  
📧 akshjainha@gmail.com  

**Aman Singh**  
💼 [LinkedIn](https://www.linkedin.com/in/amnsingh0)  
📧 amansinghakr@gmail.com  
