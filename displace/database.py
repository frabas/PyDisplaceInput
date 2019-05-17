import sqlite3
from itertools import zip_longest


class Database:
    """
    Class to manage a database with abstracted functions.
    """

    def __init__(self, file, verbose=False):
        self.__db = sqlite3.connect(file)
        self.__verbose = verbose

        self.__biosce = None
        self.__fleetsce = None
        self.__graphsce = None

    @property
    def db(self):
        return self.__db

    @property
    def biosce(self):
        return self.__biosce

    @biosce.setter
    def biosce(self, biosce):
        self.__biosce = biosce

    @property
    def fleetsce(self):
        return self.__fleetsce

    @fleetsce.setter
    def fleetsce(self, fleetsce):
        self.__fleetsce = fleetsce

    @property
    def graphsce(self):
        return self.__graphsce

    @graphsce.setter
    def graphsce(self, graphsce):
        self.__graphsce = graphsce

    def create_schema(self):
        if self.__verbose:
            print("Reading ddl from schema.ddl")

        with open("schema.ddl", mode="r") as file:
            ddl = file.read()
        self.__db.executescript(ddl)

    def create_scenario(self, name, notes):

        self._create_biosce()
        self._create_graphsce()
        self._create_fleetsce()

        c = self.__db.cursor()
        sql = "INSERT INTO Scenarios VALUES (?, ?, ?, ?, ?)"
        c.execute(sql, (name, notes, self.biosce, self.fleetsce, self.graphsce))
        self.__db.commit()

    def create_populations(self, nbpops, names=None):
        """
        Fills the populations table, with optional names (a list of names)
        """

        c = self.__db.cursor()

        sql = "INSERT INTO Populations VALUES (?, ?, ?)"

        for id, name in zip_longest(range(nbpops), names or [], fillvalue=""):
            c.execute(sql, (id, name, self.biosce))

        self.__db.commit()

    def find_all_populations_ids(self):
        c = self.db.cursor()

        sql = "SELECT id FROM Populations WHERE biosce={}".format(self.biosce)

        c.execute(sql)

        # noinspection PyShadowingBuiltins
        return (id for id, in c.fetchall())

    def insert_population_parameter(self, popid, name, value):
        c = self.__db.cursor()

        sql = "INSERT INTO PopulationParameters VALUES (?, ?, ?, ?)"
        c.execute(sql, (popid, name, value, self.biosce))

        self.__db.commit()

    def insert_config_entry(self, parameter, value):
        c = self.__db.cursor()

        sql = "INSERT INTO Config VALUES (?, ?)"
        c.execute(sql, (parameter, value))

        self.__db.commit()

    def create_nodes(self, nodes):
        c = self.db.cursor()

        sql = "INSERT INTO Nodes VALUES (?, ?, ?, ?, ?)"

        # noinspection PyShadowingBuiltins
        for id, cols in enumerate(nodes):
            c.execute(sql, (id, *cols, self.biosce))

        self.db.commit()

    def create_edges(self, edges):
        c = self.db.cursor()

        sql = "INSERT INTO Edges VALUES (?, ?, ?, ?, ?)"

        # noinspection PyShadowingBuiltins
        for id, cols in enumerate(edges):
            c.execute(sql, (id, *cols, self.biosce))

        self.db.commit()

    def _create_biosce(self):
        c = self.db.cursor()

        sql = "INSERT INTO BioSce VALUES (?)"
        c.execute(sql, (self.biosce,))

        self.db.commit()

    def _create_graphsce(self):
        c = self.db.cursor()

        sql = "INSERT INTO GraphSce VALUES (?)"
        c.execute(sql, (self.graphsce,))

        self.db.commit()

    def _create_fleetsce(self):
        c = self.db.cursor()

        sql = "INSERT INTO FleetSce VALUES (?)"
        c.execute(sql, (self.fleetsce,))

        self.db.commit()
