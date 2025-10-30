import cv2
import os
import numpy as np
from PIL import Image

def train_classifier(data_dir):
    path = [os.path.join(data_dir, f) for f in os.listdir(data_dir)]
    faces = []
    ids = []

    for folder in path:
        if not os.path.isdir(folder):  # skip if it's not a folder
            continue

        for file in os.listdir(folder):
            file_path = os.path.join(folder, file)
            if not (file_path.lower().endswith(".jpg") or file_path.lower().endswith(".png") or file_path.lower().endswith(".jpeg")):
                continue  # skip non-image files

            try:
                img = Image.open(file_path).convert('L')  # grayscale
                imageNp = np.array(img, 'uint8')
                id = int(os.path.basename(folder).split("_")[1]) if "_" in os.path.basename(folder) else 0

                faces.append(imageNp)
                ids.append(id)

            except Exception as e:
                print(f"Skipping {file_path}: {e}")

    ids = np.array(ids)

    # Train the classifier and save
    clf = cv2.face.LBPHFaceRecognizer_create()
    clf.train(faces, ids)
    clf.write("classifier.xml")
    print("✅ Training complete! Model saved as classifier.xml")

train_classifier("dataset")
