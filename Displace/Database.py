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
        return self._biosce

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

    """
    Fills the populations table, with optional names (a list of names)
    """

    def createPopulations(self, nbpops, names=None):
        c = self._db.cursor()
        for id in range(0, nbpops):
            if names is not None and len(names) > id:
                name = names[id]
            else:
                name = ""
            sql = "INSERT INTO Populations VALUES(?,?,?)"
            c.execute(sql, [id, name, self._biosce])
        self._db.commit()

    def insertPopulationParameter(self, popid, name, value):
        c = self._db.cursor()
        sql = "INSERT INTO PopulationParameters VALUES(?,?,?,?)"
        c.execute(sql, [popid, name, value, self.biosce])
        self._db.commit()

    def insertConfigEntry(self, parameter, value):
        c = self._db.cursor()
        sql = "INSERT INTO Config VALUES(?,?,?)"
        c.execute(sql, [self.biosce, parameter, value])
        self._db.commit()
