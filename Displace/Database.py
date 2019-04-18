import sqlite3

"""
Class to manage a database with abstracted functions.
"""


class Database:
    def __init__(self, file, biosce, verbose=False):
        self._db = sqlite3.connect(file)
        self._biosce = biosce
        self._verbose = verbose

    @property
    def db(self):
        return self._db

    @property
    def biosce(self):
        return self.biosce

    def createSchema(self):
        if self._verbose:
            print("Reading ddl from schema.ddl")

        with open("schema.ddl", mode="r") as file:
            ddl = file.read()
        self._db.executescript(ddl)

    def createScenario(self, biosce_name, biosce_notes):
        c = self._db.cursor()
        sql = "INSERT INTO Scenarios VALUES(?,?,?)"
        c.execute(sql, [self._biosce, biosce_name, biosce_notes])
        self._db.commit()
