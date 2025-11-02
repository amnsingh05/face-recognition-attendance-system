import cv2
import os
import datetime
import pandas as pd

# Paths
DATASET_DIR = "faces"
TRAINER_PATH = os.path.join("trainer", "trainer.yml")
ATTENDANCE_FILE = "attendance.csv"

# Ensure attendance file exists
if not os.path.exists(ATTENDANCE_FILE):
    df = pd.DataFrame(columns=["Name", "Date", "Time"])
    df.to_csv(ATTENDANCE_FILE, index=False)


def mark_attendance(name):
    """Add attendance entry for recognized person"""
    now = datetime.datetime.now()
    date = now.strftime("%Y-%m-%d")
    time = now.strftime("%H:%M:%S")

    # Ensure attendance file exists with proper columns
    if not os.path.exists(ATTENDANCE_FILE):
        df = pd.DataFrame(columns=["Name", "Date", "Time"])
        df.to_csv(ATTENDANCE_FILE, index=False)

    df = pd.read_csv(ATTENDANCE_FILE)

    # ✅ If CSV exists but missing required columns — fix it
    expected_cols = {"Name", "Date", "Time"}
    if not expected_cols.issubset(df.columns):
        print("⚠️ Fixing corrupted attendance.csv structure...")
        df = pd.DataFrame(columns=["Name", "Date", "Time"])
        df.to_csv(ATTENDANCE_FILE, index=False)

    # Avoid duplicate marking for same day
    if not ((df["Name"] == name) & (df["Date"] == date)).any():
        df.loc[len(df)] = [name, date, time]
        df.to_csv(ATTENDANCE_FILE, index=False)
        print(f"✅ Attendance marked for {name} at {time}")
    else:
        print(f"ℹ️ {name} already marked today.")


def take_attendance():
    """Start face recognition attendance"""
    if not os.path.exists(TRAINER_PATH):
        print("❌ trainer.yml not found. Run train_model.py first.")
        return

    recognizer = cv2.face.LBPHFaceRecognizer_create()
    recognizer.read(TRAINER_PATH)
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")

    # Map numeric labels to folder names (user names)
    label_dict = {i: name for i, name in enumerate(os.listdir(DATASET_DIR))}

    cam = cv2.VideoCapture(0)
    if not cam.isOpened():
        print("❌ Could not access the camera.")
        return

    print("🎥 Face Attendance started. Press 'q' to quit.\n")

    while True:
        ret, frame = cam.read()
        if not ret:
            break

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.3, 5)

        for (x, y, w, h) in faces:
            id_, confidence = recognizer.predict(gray[y:y+h, x:x+w])
            name = label_dict.get(id_, "Unknown")

            # Draw rectangle & text
            cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
            cv2.putText(frame, f"{name} ({round(confidence, 2)})", (x, y-10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)

            if confidence < 80 and name != "Unknown":
                mark_attendance(name)

        cv2.imshow("Face Attendance", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cam.release()
    cv2.destroyAllWindows()
    print("\n🟢 Attendance recording stopped.")


if __name__ == "__main__":
    take_attendance()
