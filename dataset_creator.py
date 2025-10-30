import cv2
import os

# Create folder for dataset if not exists
dataset_path = 'dataset'
if not os.path.exists(dataset_path):
    os.makedirs(dataset_path)

# Ask for user ID or name
user_name = input("Enter your name: ")

# Create subfolder for the user
user_folder = os.path.join(dataset_path, user_name)
if not os.path.exists(user_folder):
    os.makedirs(user_folder)

# Initialize camera
cam = cv2.VideoCapture(0)
face_detector = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

print("Capturing images... Look at the camera and wait")

count = 0
while True:
    ret, frame = cam.read()
    if not ret:
        break

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_detector.detectMultiScale(gray, 1.3, 5)

    for (x, y, w, h) in faces:
        count += 1
        face = gray[y:y+h, x:x+w]
        cv2.imwrite(f"{user_folder}/{count}.jpg", face)
        cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)
        cv2.imshow('Capturing Faces', frame)

    # Stop if 'q' pressed or 50 images taken
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    elif count >= 50:
        break

print(f"\n{count} images saved for {user_name}")
cam.release()
cv2.destroyAllWindows()
