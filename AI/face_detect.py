import cv2


class FaceDetect:
    def __init__(self):
        self.image = None
        self.faces = None
        self.cascade_path = "./models/haarcascade_frontalface_default.xml"
        self.face_cascade = cv2.CascadeClassifier(self.cascade_path)

    def faces_detect(self, image_path):
        # Read the image
        self.image = cv2.imread(image_path)
        gray = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)

        # Detect faces in the image
        self.faces = self.face_cascade.detectMultiScale(
            gray,
            scaleFactor=1.1,
            minNeighbors=5,
            minSize=(30, 30),
            flags=cv2.CASCADE_SCALE_IMAGE
        )

        return self.faces

    def draw_box(self):

        print("Found {0} faces!".format(len(self.faces)))

        for (x, y, w, h) in self.faces:
            cv2.rectangle(self.image, (x, y), (x + w, y + h), (0, 255, 0), 2)

        return cv2.cvtColor(self.image, cv2.COLOR_BGR2RGB)
