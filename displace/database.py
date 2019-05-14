import sqlite3


class Database:
    """
    Class to manage a database with abstracted functions.
    """

    def __init__(self, file, biosce, verbose=False):
        self.__db = sqlite3.connect(file)
        self.__biosce = biosce
        self.__verbose = verbose

    @property
    def db(self):
        return self.__db

    @property
    def biosce(self):
        return self.__biosce

    def create_schema(self):
        if self.__verbose:
            print("Reading ddl from schema.ddl")

        with open("schema.ddl", mode="r") as file:
            ddl = file.read()
        self.__db.executescript(ddl)

    def create_scenario(self, biosce_name, biosce_notes):
        c = self.__db.cursor()
        sql = "INSERT INTO Scenarios VALUES(?,?,?)"
        c.execute(sql, [self.__biosce, biosce_name, biosce_notes])
        self.__db.commit()

    def create_populations(self, nbpops, names=None):
        """
        Fills the populations table, with optional names (a list of names)
        """

        c = self.__db.cursor()

        # noinspection PyShadowingBuiltins
        for id in range(0, nbpops):
            if names is not None and len(names) > id:
                name = names[id]
            else:
                name = ""
            sql = "INSERT INTO Populations VALUES(?,?,?)"
            c.execute(sql, [id, name, self.__biosce])
        self.__db.commit()

    def insert_population_parameter(self, popid, name, value):
        c = self.__db.cursor()
        sql = "INSERT INTO PopulationParameters VALUES(?,?,?,?)"
        c.execute(sql, [popid, name, value, self.biosce])
        self.__db.commit()

    def insert_config_entry(self, parameter, value):
        c = self.__db.cursor()
        sql = "INSERT INTO Config VALUES(?,?,?)"
        c.execute(sql, [self.biosce, parameter, value])
        self.__db.commit()
