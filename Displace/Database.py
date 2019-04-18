import sqlite3

"""
Class to manage a database with abstracted functions.
"""


class Database:
    def __init__(self, file, biosce, verbose=False):
        self.db = sqlite3.connect(file)
        self.biosce = biosce
        self.verbose = verbose

    def createSchema(self):
        if self.verbose:
            print("Reading ddl from schema.ddl")

        with open("schema.ddl", mode="r") as file:
            ddl = file.read()
        self.db.executescript(ddl)

    def createScenario(self, biosce_name, biosce_notes):
        c = self.db.cursor()
        sql = "INSERT INTO Scenarios VALUES(?,?,?)"
        c.execute(sql, [self.biosce, biosce_name, biosce_notes])
        self.db.commit()
      