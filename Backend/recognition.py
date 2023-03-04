import face_recognition
from PIL import Image, ImageDraw

"""Returns the encoding for a student's face
"""
def encode_student(image_path: str) -> list:
    loaded_picture = face_recognition.load_image_file(image_path)
    encoding = face_recognition.face_encodings(loaded_picture)
    if len(encoding) > 0:
        return encoding[0]
    return None

def take_attendance(image_path: str, students: dict) -> list:
    t = 0.4
    
    # Load the student photos to numpy format for comparisons
    present_students = dict()
    for id in students:
        if students[id]["encoding"] is not None:
            present_students[id] = None

    loaded_class_photo = face_recognition.load_image_file(image_path)
    # find the face locations
    face_locations = face_recognition.face_locations(
        img = loaded_class_photo,
        number_of_times_to_upsample = 1,
        model = "small"
    )
    # with Image.open(image_path).convert("RGB") as image:
    #     canvas = ImageDraw.Draw(image)
    #     for face in face_locations:
    #         x, y, w, h = face
    #         canvas.rectangle(((y, x), (h, w)), outline="red")
    #         image.save(image_path, "JPEG")
    
    
    # can change num_jitters and model to become more accurate but also slower
    face_encodings = face_recognition.face_encodings(
        face_image = loaded_class_photo,
        known_face_locations = face_locations,
        num_jitters = 1,
        model = "large"
    )

    faces = []

    for id in present_students:
        matches = face_recognition.compare_faces(face_encodings, students[id]['encoding'], tolerance=t)
        # ignoring the case that there are > 1 matches for now
        if True in matches:
            index = matches.index(True)
            location = face_locations[index]
            face = {
                "x": location[0],
                "y": location[1],
                "width": location[2],
                "height": location[3],
                "student": id
            }
            faces.append(face)

    print(image_path)
    #mark up the class photo and draw rectangles around each face with the name
    with Image.open(image_path).convert("RGB") as image:
        canvas = ImageDraw.Draw(image)
        for face in faces:
            x, y, w, h, id = face["x"], face["y"], face["width"], face["height"], face["student"]
            #print(x, y, w, h)
            canvas.rectangle(((y, x), (h, w)), outline="red")
            #print(students)
            message = students[id]["first_name"] + " " + students[id]["last_name"]
            text_w, text_h = canvas.textsize(message)
            canvas.text((y+h+text_h, x+w//2-text_w//2), message, fill="red")
            image.save(image_path, "JPEG")

    # but in json format right? or do we draw the bounding boxes in
    return faces
    