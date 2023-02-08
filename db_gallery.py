import os
import pickle
import sqlite3

from PySide6.QtGui import QPixmap, QImage


def toQPixmap(raw_bytes):
    image = QImage(raw_bytes, 128, 128, QImage.Format.Format_RGB888)
    return QPixmap.fromImage(image)


def unRaw(raw_bytes):
    return pickle.loads(raw_bytes)


class DbGallery:
    def __init__(self, gallery_path, db_name=".thumbnails.db"):
        self.cursor = None
        self.connection = None
        self.gallery_file = None
        self.db_name = db_name
        self.gallery_path = gallery_path
        self.gallery_file = os.path.join(self.gallery_path, self.db_name)

    def open(self):
        self.connection = sqlite3.connect(self.gallery_file)
        self.cursor = self.connection.cursor()
        self._create_schema()

    def exists(self):
        if os.path.exists(self.gallery_file):
            return True
        return False

    def insertBlob(self, data):
        query = "INSERT INTO faces(file, bytes, encodings, landmarks) VALUES(?, ?, ?, ?)"
        self.cursor.executemany(query, data)
        self.connection.commit()

    def test_fetch(self, query):
        return self.connection.execute(query).fetchall()

    def fetch(self, query):
        return [{
            'file': row[0],
            'match': row[1],
            'tags': row[2],
            'pixmap': toQPixmap(row[3]),
            'encodings': pickle.loads(row[4]),
            'landmarks': pickle.loads(row[5]),
            'path': os.path.join(self.gallery_path, row[0])
        } for row in self.connection.execute(query).fetchall()]

    def fetchAllFaces(self):
        return self.fetch("SELECT * FROM faces")

    def fetchBy(self, file_name):
        query = "SELECT * FROM faces WHERE file = '%s'" % file_name
        return self.fetch(query)[0]

    def fetch_tags(self):
        query = "SELECT * FROM faces WHERE match IS NOT NULL AND TRIM(match,' ') != '' GROUP BY match"
        return self.fetch(query)

    def fetch_tagged(self, file_name):
        query = "SELECT * FROM faces WHERE match = '%s'" % file_name
        print(query)
        return self.fetch(query)

    def updateAll(self, values):
        query = "UPDATE faces SET match = ?, tags = ? WHERE file = ?"
        self.cursor.executemany(query, values)
        self.connection.commit()

    def deleteBy(self, value):
        query = "DELETE FROM faces WHERE file = ?"
        self.connection.executemany(query, value)
        self.connection.commit()

    def close(self):
        self.connection.close()

    def _create_schema(self):
        table_faces = "CREATE TABLE IF NOT EXISTS faces(file TEXT NOT NULL UNIQUE , " \
                      "match TEXT, tags TEXT, bytes BLOB, encodings BLOB, landmarks BLOB, PRIMARY KEY (file))"

        self.cursor.execute(table_faces)
