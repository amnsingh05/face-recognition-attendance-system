import cv2
import os
import numpy as np
from PIL import Image
from datetime import datetime
import pandas as pd
import tkinter as tk
from tkinter import messagebox

# ==============================
# Helper Functions
# ==============================
def mark_attendance(name, username):
    """
    Save attendance entry for recognized user
    """
    folder = "teachers_attendance"
    os.makedirs(folder, exist_ok=True)

    file_path = os.path.join(folder, f"{username}_attendance.csv")

    # Create CSV file if it doesn't exist
    if not os.path.exists(file_path):
        df = pd.DataFrame(columns=["Name", "Username", "Date", "Time"])
        df.to_csv(file_path, index=False)

    now = datetime.now()
    date = now.strftime("%Y-%m-%d")
    time = now.strftime("%H:%M:%S")

    df = pd.read_csv(file_path)

    # Prevent duplicate attendance for same day
    if not ((df["Username"] == username) & (df["Date"] == date)).any():
        new_entry = pd.DataFrame([[name, username, date, time]],
                                 columns=["Name", "Username", "Date", "Time"])
        df = pd.concat([df, new_entry], ignore_index=True)
        df.to_csv(file_path, index=False)
        print(f"✅ Attendance marked for {name} at {time}")
    else:
        print(f"ℹ️ Attendance already marked for {name} today.")


# ==============================
# Main Attendance Function
# ==============================
def start_attendance(username):
    """
    Starts webcam, detects faces, and marks attendance.
    """
    # --- Check if trained model exists ---
    if not os.path.exists("classifier.xml"):
        messagebox.showerror("Error", "Model not trained! Please train model first.")
        return

    # Load trained classifier and face detector
    recognizer = cv2.face.LBPHFaceRecognizer_create()
    recognizer.read("classifier.xml")
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")

    # --- Start webcam ---
    cap = cv2.VideoCapture(0)

    messagebox.showinfo("Attendance", "Press 'Q' to exit camera after attendance capture.")

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.3, 5)

        for (x, y, w, h) in faces:
            id_, conf = recognizer.predict(gray[y:y+h, x:x+w])
            conf = 100 - int(conf)

            if conf > 70:
                name = f"User_{id_}"  # placeholder (we can link this to dataset names)
                mark_attendance(name, username)
                color = (0, 255, 0)
                label = f"{name} ({conf}%)"
            else:
                color = (0, 0, 255)
                label = "Unknown"

            cv2.rectangle(frame, (x, y), (x + w, y + h), color, 2)
            cv2.putText(frame, label, (x, y - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.8, color, 2)

        cv2.imshow("Face Recognition Attendance", frame)

        # Press Q to exit
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
    messagebox.showinfo("Attendance", "Attendance process completed successfully!")


# ==============================
# Run directly for testing
# ==============================
if __name__ == "__main__":
    # Replace 'teacher1' with the currently logged-in username when integrating with login_gui.py
    start_attendance("teacher1")
