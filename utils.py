import os
import pickle

import PIL.Image
import face_recognition
import filetype
import numpy as np
from PySide6.QtGui import QImage, QPixmap


def serialize(data):
    return pickle.dumps(data, protocol=5)


def getPath(folder_path, file):
    return os.path.join(folder_path, file)


def rawToQPixmap(raw_bytes):
    image = QImage(raw_bytes, 128, 128, QImage.Format.Format_RGB888)
    return QPixmap.fromImage(image)


def imageOpen(image_file):
    image_file = os.path.join(image_file)
    image = PIL.Image.open(image_file)
    return image.convert('RGB')


def imageThumbnail(image):
    image.thumbnail((128, 128), PIL.Image.ANTIALIAS)
    return image.tobytes()


def npArray(image):
    return np.array(image)


def scanFolderImages(folder_path):
    image_list = []
    for file in os.listdir(folder_path):
        image_file = os.path.join(folder_path, file)
        if os.path.isfile(image_file):
            if filetype.is_image(image_file):
                image_list.append(file)
    return image_list


def faceEncodings(face):
    try:
        encodings = face_recognition.face_encodings(face)
        return serialize(encodings)
    except IndexError:
        return None


def faceLandmarks(face):
    try:
        landmarks = face_recognition.face_landmarks(face)
        return serialize(landmarks)
    except IndexError:
        return None


def compareFaces(known_face, unknown_face):
    try:
        return face_recognition.compare_faces(known_face, unknown_face[0])[0]
    except IndexError:
        return False


# def pil2pixmap(self, im):
#     if im.mode == "RGB":
#         r, g, b = im.split()
#         im = Image.merge("RGB", (b, g, r))
#     elif im.mode == "RGBA":
#         r, g, b, a = im.split()
#         im = Image.merge("RGBA", (b, g, r, a))
#     elif im.mode == "L":
#         im = im.convert("RGBA")
#     # Bild in RGBA konvertieren, falls nicht bereits passiert
#     im2 = im.convert("RGBA")
#     data = im2.tobytes("raw", "RGBA")
#     qim = QtGui.QImage(data, im.size[0], im.size[1], QtGui.QImage.Format_ARGB32)
#     pixmap = QtGui.QPixmap.fromImage(qim)
#     return pixmap
