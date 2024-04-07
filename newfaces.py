import tkinter as tk
from tkinter import Entry, Button
import cv2
import face_recognition
import os
import numpy as np
from PIL import Image, ImageTk

def capture_faces(name_entry, images_directory="D:/Coding/mini project/images", database_directory="D:/Coding/mini project/database"):
    name = name_entry.get()

    if not name:
        print("Please enter a name.")
        return

    # Create directories if they don't exist
    os.makedirs(images_directory, exist_ok=True)

    # Capture faces
    encodings_to_save = []  
    for i in range(10):
        capture = cv2.VideoCapture(0, cv2.CAP_DSHOW)
        face_detected = False

        while not face_detected:
            _, frame = capture.read()
            cv2.imshow("Capture", frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

            # Check if a face is detected
            face_locations = face_recognition.face_locations(frame)

            if face_locations:
                # Save captured face
                image_path = os.path.join(images_directory, f"{name}_{i}.jpg")
                cv2.imwrite(image_path, frame)
                print(f"Captured face {i + 1}")

                # Save the encoding to be included in the data file
                encoding = face_recognition.face_encodings(frame)[0]
                encodings_to_save.append(encoding)

                face_detected = True
            else:
                # If no face is detected, display a message
                cv2.putText(frame, "No face detected", (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)
                cv2.imshow("Capture", frame)

        capture.release()

    # Save encodings and names directly to a text file (data.txt)
    data_file_path = os.path.join(database_directory, "data.txt")
    with open(data_file_path, mode='a', newline='') as data_file:
        for encoding in encodings_to_save[:7]:
            data_file.write(f"{name},{','.join(map(str, encoding))}\n")

    cv2.destroyAllWindows()
    print(f"Capturing faces for {name} completed.")

class FaceCaptureApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Face Capture App")

        self.name_label = tk.Label(root, text="Enter Name:")
        self.name_label.pack()

        self.name_entry = Entry(root)
        self.name_entry.pack()

        self.add_photos_button = Button(root, text="Capture Face", command=self.AddFaceButtonPressed)
        self.add_photos_button.pack()

    def AddFaceButtonPressed(self):
        capture_faces(self.name_entry)

def executeAdd():
    root = tk.Tk()
    app = FaceCaptureApp(root)
    root.mainloop()

if __name__ == "__main__":
    executeAdd()