import sqlite3

"""
Class to manage a database with abstracted functions.
"""


class Database:
    def __init__(self, file, verbose=False):
        self.db = sqlite3.connect(file)
        self.verbose = verbose

    def createSchema(self):
        if self.verbose:
            print("Reading ddl from schema.ddl")

        with open("schema.ddl", mode="r") as file:
            ddl = file.read()
        self.db.executescript(ddl)
