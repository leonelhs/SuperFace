import contextlib
import os
from sqlite3 import connect

from PIL import Image
# import pillow_avif

from AI.face_tagger import FaceTagger
from Storage import Storage

import pickle

folder = "/Users/leonel/rbox/"


def rename():
    for filename in os.listdir(folder):
        in_filename = os.path.join(folder, filename)
        if not os.path.isfile(in_filename):
            continue
        if in_filename.endswith(".jpg_large"):
            newname = in_filename.replace('.jpg_large', '.jpg')
            print(newname)
            os.rename(in_filename, newname)


def convert_avif():
    for filename in os.listdir(folder):
        in_filename = os.path.join(folder, filename)
        if not os.path.isfile(in_filename):
            continue
        if in_filename.endswith(".avif"):
            newname = in_filename.replace('.avif', '.png')
            image = Image.open(in_filename)
            print(newname)
            image.save(newname, "png")


path = "/home/leonel/politica"
img0 = "70976760_1376585805852472_8808327691593126489_n.jpg"
img1 = "28428706_418452788597362_5477947764883062784_n.jpg"
img_test = os.path.join(path, img0)


class Faces:

    def __init__(self):
        self.faceTagger = None
        self.dbGallery = None

    def testFaces(self):
        self.faceTagger = FaceTagger()
        self.dbGallery = Storage(path)
        self.dbGallery.open()
        image_list = self.dbGallery.fetchAllFaces()
        print(image_list[0])

    def testFace(self):
        self.faceTagger = FaceTagger()
        self.faceTagger.setKnownFace(img_test)
        encodings = self.faceTagger.faceEncodings()

        blob = pickle.dumps(encodings, protocol=5)

        self.faceTagger = FaceTagger()
        self.dbGallery = Storage(path)
        self.dbGallery.open()
        self.dbGallery.insertFaces([("blob", blob)])
        self.dbGallery.close()

    def test_blobs(self):
        self.dbGallery = Storage(path)
        self.dbGallery.open()
        result = self.dbGallery.test_fetch("SELECT * FROM faces WHERE file = 'blob'")
        new_blob = pickle.loads(result[0][3])
        print(new_blob)


def test_base():
    db_name = "test.db"
    with contextlib.closing(connect(db_name)) as con:
        with con as cur:
            cur.executescript("""
            CREATE TABLE IF NOT EXISTS galleries(
                path TEXT NOT NULL UNIQUE , 
                opened DATETIME, 
                PRIMARY KEY (path));
            """)


test_base()
