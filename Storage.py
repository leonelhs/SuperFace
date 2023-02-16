import contextlib
from datetime import datetime
from sqlite3 import connect as connect


class DbConnection(contextlib.closing):
    def __init__(self, db_name):
        self.thing = connect(db_name)
        super().__init__(self.thing)


class Storage:
    def __init__(self, db_name=".images.db"):
        self._gallery_id = None
        self._gallery_path = None
        self._db_name = db_name
        self._create_schema()

    def path(self):
        return self._gallery_path

    def insertRecent(self, file_path):
        with DbConnection(self._db_name) as con:
            with con as cur:
                data = (file_path, datetime.now())
                try:
                    cur.execute("INSERT INTO recents(photo_id, opened) VALUES(?, ?)", data)
                except:
                    pass

    def fetchRecents(self):
        with DbConnection(self._db_name) as con:
            with con as cur:
                query = "SELECT photo_id FROM recents ORDER BY opened DESC LIMIT 10"
                return cur.execute(query).fetchall()

    def _create_schema(self):
        with DbConnection(self._db_name) as con:
            with con as cur:
                cur.executescript("""
                CREATE TABLE IF NOT EXISTS recents(
                    photo_id TEXT NOT NULL UNIQUE,
                    opened DATETIME);
                """)
