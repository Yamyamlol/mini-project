import face_recognition
import cv2
import numpy as np
import csv
import os
from datetime import datetime

def save_to_csv(names, encodings, directory):
    today_date = datetime.now().strftime("%d-%m-%Y")
    csv_file_path = os.path.join(directory, f"Attendance_of_{today_date}.csv")

    existing_dates = set()

    with open(csv_file_path, mode='a', newline='') as file:
        writer = csv.writer(file)

        if os.path.exists(csv_file_path) and os.stat(csv_file_path).st_size != 0:
            with open(csv_file_path, mode='r') as read_file:
                reader = csv.reader(read_file)
                next(reader, None)
                for row in reader:
                    existing_dates.add((row[0], row[2]))

        if not existing_dates:
            writer.writerow(["Name", "Time", "Date"])

        for name in names:
            now = datetime.now()
            current_time = now.strftime("%H:%M:%S")
            current_date = now.strftime("%d-%m-%Y")

            if (name, current_date) not in existing_dates:
                writer.writerow([name, current_time, current_date])
                existing_dates.add((name, current_date))

    return csv_file_path

def read_encodings_from_data(file_path):
    names, encodings = [], []
    with open(file_path, mode='r') as file:
        reader = csv.reader(file)
        for row in reader:
            names.append(row[0])
            encoding_values = [float(value) for value in row[1:]]
            encoding = np.array(encoding_values)
            encodings.append(encoding)
    return names, encodings

def mark_attendance_with_face_recognition(data_file_path, destination_directory):
    known_faces_names, known_face_encodings = read_encodings_from_data(data_file_path)
    students = known_faces_names.copy()
    display_positions = {}

    video_capture = cv2.VideoCapture(0, cv2.CAP_DSHOW)

    while True:
        _, frame = video_capture.read()
        small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
        rgb_small_frame = cv2.cvtColor(small_frame, cv2.COLOR_BGR2RGB)

        face_locations = face_recognition.face_locations(rgb_small_frame)
        face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)
        face_names = []

        for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
            matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
            name = "Unknown"

            face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
            best_match_index = np.argmin(face_distances)

            if matches[best_match_index] and face_distances[best_match_index] < 0.5:
                name = known_faces_names[best_match_index]

            face_names.append(name)

            # Draw a rectangle around the face
            cv2.rectangle(frame, (left * 4, top * 4), (right * 4, bottom * 4), (0, 255, 0), 2)

            if name == "Unknown":
                font = cv2.FONT_HERSHEY_SIMPLEX
                font_scale = 0.5
                font_color = (0, 0, 255)
                thickness = 1
                line_type = 2
                bottom_left_corner_of_text = (left * 4, bottom * 4 + 20)
                cv2.putText(frame, "Unknown", bottom_left_corner_of_text, font, font_scale, font_color, thickness, line_type)
            else:
                font = cv2.FONT_HERSHEY_COMPLEX
                font_scale = 0.5
                font_color = (0, 0, 255)
                thickness = 1
                line_type = 2

                # Use a unique position for each name
                if name not in display_positions:
                    display_positions[name] = len(display_positions) + 1

                bottom_left_corner_of_text = (10, 100 + 30 * display_positions[name])

                cv2.putText(frame, f"{name} Present",
                            bottom_left_corner_of_text,
                            font,
                            font_scale,
                            font_color,
                            thickness,
                            line_type)

                if name in students:
                    students.remove(name)
                    now = datetime.now()
                    current_date = now.strftime("%Y-%m-%d")
                    print(f"Marking attendance for {name} at {current_date} {now.strftime('%H:%M:%S')}")
                    save_to_csv([name], [known_face_encodings[best_match_index]], destination_directory)

        cv2.imshow("Face Recognition", frame)
        key = cv2.waitKey(1)
        if key == ord('q') or key == 27:  # 27 is the ASCII code for the ESC key
            break

    video_capture.release()
    cv2.destroyAllWindows()

def mark_attendance_button_pressed():
    """
    Function to mark attendance using face recognition.
    """
    # Specify the path to the CSV file
    data_file_path = os.path.join('D:/Coding/mini project/database', "Data.txt")

    # Specify the path to the destination directory
    destination_directory = "D:/Coding/mini project/Attendance"

    # Call the face recognition function
    mark_attendance_with_face_recognition(data_file_path, destination_directory)
    
if __name__ == "__main__":
    mark_attendance_button_pressed()
