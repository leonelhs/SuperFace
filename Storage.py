import contextlib
from datetime import datetime
from sqlite3 import connect as connect

from Face import Face


class DbConnection(contextlib.closing):
    def __init__(self, db_name):
        self.thing = connect(db_name)
        super().__init__(self.thing)


class Storage:
    def __init__(self, db_name=".gallery.db"):
        self._gallery_id = None
        self._gallery_path = None
        self._db_name = db_name
        self._create_schema()

    def path(self):
        return self._gallery_path

    def open(self, gallery_path):
        self._gallery_path = gallery_path
        with DbConnection(self._db_name) as con:
            with con as cur:
                try:
                    query = "SELECT gallery_id FROM galleries WHERE path = ?"
                    self._gallery_id = cur.execute(query, (self._gallery_path,)).fetchone()[0]
                    if self._gallery_path:
                        return True
                except:
                    pass
                    return False

    def insertFaces(self, values):
        with DbConnection(self._db_name) as con:
            with con as ins:
                data = (hash(self._gallery_path), self._gallery_path, datetime.now())
                ins.execute("INSERT INTO galleries(gallery_id, path, opened) VALUES(?, ?, ?)", data)
            with con as cur:
                query = "INSERT INTO faces(gallery_id, face_id, thumbnail, encodings, landmarks) VALUES(?, ?, ?, ?, ?)"
                cur.executemany(query, values)
                con.commit()

    def fetchGalleries(self):
        with DbConnection(self._db_name) as con:
            with con as cur:
                query = "SELECT path FROM galleries ORDER BY opened DESC LIMIT 10"
                return cur.execute(query).fetchall()

    def fetchAllFaces(self):
        with DbConnection(self._db_name) as con:
            with con as cur:
                query = "SELECT path||'/'||face_id, " \
                        "faces.gallery_id, face_id, match, tags, thumbnail, encodings, landmarks " \
                        "FROM faces INNER JOIN galleries ON galleries.gallery_id = faces.gallery_id " \
                        "AND faces.gallery_id = ?"
                result = cur.execute(query, (self._gallery_id,)).fetchall()
                return [Face(*row) for row in result]

    def fetchFaceBy(self, face_id):
        with DbConnection(self._db_name) as con:
            with con as cur:
                query = "SELECT * FROM faces WHERE gallery_id = ? AND face_id = ?"
                return cur.execute(query, (self._gallery_id, face_id)).fetchone()

    def updateAll(self, values):
        with DbConnection(self._db_name) as con:
            with con as cur:
                query = "UPDATE faces SET tags = ? WHERE gallery_id = ? AND face_id = ?"
                cur.executemany(query, values)
                con.commit()

    def _create_schema(self):
        with DbConnection(self._db_name) as con:
            with con as cur:
                cur.executescript("""
                CREATE TABLE IF NOT EXISTS galleries(
                    gallery_id TEXT NOT NULL UNIQUE,
                    path TEXT NOT NULL UNIQUE , 
                    opened DATETIME, 
                    PRIMARY KEY (gallery_id));
                    
                CREATE TABLE IF NOT EXISTS faces(
                    gallery_id TEXT NOT NULL,
                    face_id TEXT NOT NULL,
                    match INTEGER, 
                    tags TEXT, 
                    thumbnail BLOB, 
                    encodings BLOB, 
                    landmarks BLOB, 
                    PRIMARY KEY (gallery_id, face_id));
                """)
