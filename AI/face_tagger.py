import os

import PIL.Image
import face_recognition
import numpy as np


def to_pil_image(gallery_path, file):
    file_path = os.path.join(gallery_path, file)
    image = PIL.Image.open(file_path)
    return image.convert('RGB')


class FaceTagger:
    def __init__(self, callback_logger=None):
        self.pil_image = None
        self.person_encoding = None
        self.known_face = None
        self.logger = callback_logger

    def setKnownFace(self, pil_image):
        self.pil_image = pil_image
        self.known_face = np.array(self.pil_image)

    def faceEncodings(self):
        try:
            return face_recognition.face_encodings(self.known_face)
        except IndexError:
            self.logger("No face encodings detected at ", self.known_face)

    def faceLandmarks(self):
        try:
            return face_recognition.face_landmarks(self.known_face)
        except IndexError:
            self.logger("No face landmarks detected at ", self.known_face)

    def compareFaces(self, known_face, unknown_face):
        try:
            print("unknown photo has %d faces" % len(unknown_face))
            return face_recognition.compare_faces([known_face], unknown_face[0])
        except IndexError:
            self.logger("No faces match at ", unknown_face)
            return False

    def checkUnknownFace(self, file_face):
        try:
            self.person_encoding = self.faceEncodings()
            unknown_face = face_recognition.load_image_file(file_face)
            unknown_encoding = face_recognition.face_encodings(unknown_face)[0]
            return face_recognition.compare_faces([self.person_encoding], unknown_encoding)[0]
        except IndexError:
            self.logger("No face match at ", file_face)
            return False

