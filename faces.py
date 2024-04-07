import tkinter as tk
from tkinter import filedialog
import face_recognition
import shutil
import cv2
import os
import csv
import numpy as np
from PIL import Image, ImageTk
class ArrayManager:
    encodings = []
    names = []
def copy_to_directory(image, name, destination_directory, image_number):
    if not os.path.exists(destination_directory):
        os.makedirs(destination_directory)
    destination_path = os.path.join(destination_directory, f"{name}{image_number}.jpg")
    cv2.imwrite(destination_path, image)
    print(f'The captured image has been saved to {destination_path}')
    return destination_path
def save_to_csv(names, encodings, csv_file_path):
    file_exists = os.path.exists(csv_file_path)
    with open(csv_file_path, mode='a', newline='') as file:
        writer = csv.writer(file)
        if not file_exists or os.stat(csv_file_path).st_size == 0:
            writer.writerow(["Name", "Encoding"])
        for name, encoding in zip(names, encodings):
            encoding = encoding / np.linalg.norm(encoding)
            encoding_strings = [str(value) for value in encoding]
            writer.writerow([name] + encoding_strings)
    return csv_file_path
def capture_images(array_manager, name_entry, destination_directory, capture_interval):
    if len(array_manager.names) > 0:
        print("You have already entered a name.")
        return
    name = name_entry.get()
    if not name:
        print("Please enter a name.")
        return
    cap = cv2.VideoCapture(0)
    cv2.namedWindow("Capture Face", cv2.WINDOW_NORMAL)
    face_count = 0
    def capture_frame():
        nonlocal face_count
        ret, frame = cap.read()
        face_locations = face_recognition.face_locations(frame)
        if face_locations:
            encoding = face_recognition.face_encodings(frame, face_locations)[0]
            array_manager.names.append(name)
            array_manager.encodings.append(encoding)
            print("Names:", array_manager.names)
            print("Encodings:", array_manager.encodings)
            destination_directory = os.path.abspath(destination_directory)
            destination_path = copy_to_directory(frame, name, destination_directory, face_count + 1)
            csv_file_path = save_to_csv(array_manager.names, array_manager.encodings, os.path.join(destination_directory, "Data.txt"))
            print(f'Data has been saved to {csv_file_path}')
            face_count += 1
            if face_count < 10:
                # Convert the OpenCV image to a Tkinter-compatible format using PIL
                pil_image = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
                tk_image = ImageTk.PhotoImage(pil_image)
                label.config(image=tk_image)
                label.image = tk_image
                
                root.after(capture_interval, capture_frame)  # Schedule the next capture
        else:
            print("No face found in the captured image.")
    root = tk.Tk()
    root.title("Add a New Face")
    label = tk.Label(root)
    label.pack()
    capture_frame()  # Start the first capture
    root.after(capture_interval, capture_frame)  # Schedule the next capture
    root.mainloop()
# Do not call add_new_face() here
def add_new_face():
    destination_directory = "D:/Coding/mini project/images"

    name_entry = tk.Entry()
    name_entry.place(relx = 0.6, rely = 0.6, width = 80, height = 40)

    add_face_button = tk.Button(text="Add Face", cursor="hand2", command=lambda: capture_images(ArrayManager(), name_entry, destination_directory, capture_interval=500))
    add_face_button.pack()

    tk.mainloop()