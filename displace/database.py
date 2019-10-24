import sqlite3
import os
from itertools import zip_longest


class Database:
    """
    Class to manage a database with abstracted functions.
    """

    def __init__(self, file, verbose=False):
        self.__db = sqlite3.connect(file)
        self.__verbose = verbose

        self.biosce = None
        self.fleetsce = None
        self.graphsce = None

    @property
    def db(self):
        return self.__db

    def create_schema(self, mainpath):
        if self.__verbose:
            print("Reading ddl from schema.ddl")

        schemafile = os.path.join(mainpath, "schema.ddl")
        with open(schemafile, mode="r") as file:
            ddl = file.read()
        self.__db.executescript(ddl)

    def create_scenario(self, name, notes):
        self.__create_biosce()
        self.__create_graphsce()
        self.__create_fleetsce()
        self.__current_scenario = name

        c = self.__db.cursor()
        sql = "INSERT INTO Scenarios VALUES (?, ?, ?, ?, ?)"
        c.execute(sql, (name, notes, self.biosce, self.fleetsce, self.graphsce))
        self.__db.commit()

    # noinspection PyDefaultArgument
    def create_populations(self, nbpops, names=[]):
        """
        Fills the populations table, with optional names (a list of names)
        """

        c = self.__db.cursor()

        sql = "INSERT INTO Populations VALUES (?, ?, ?)"

        for id, name in zip_longest(range(nbpops), names, fillvalue=""):
            c.execute(sql, (id, name, self.biosce))

        self.__db.commit()

    def find_all_populations_ids(self):
        c = self.db.cursor()

        sql = "SELECT id FROM Populations WHERE biosce={}".format(self.biosce)

        c.execute(sql)

        # noinspection PyShadowingBuiltins
        # Unpack id from rows
        return (id for id, in c.fetchall())

    def insert_population_parameter(self, popid, name, value, period=None, country=None):
        c = self.__db.cursor()

        sql = "INSERT INTO PopulationParameters VALUES (?, ?, ?, ?, ?, ?)"
        c.execute(sql, (popid, name, value, self.biosce, period, country))

        self.__db.commit()

    def insert_population_parameter_with_szgroup_and_age(self, popid, name, value, szgroup=None, age=None, period=None, node=None):
        c = self.__db.cursor()

        sql = "INSERT INTO PopulationParametersWithSizeGroupAndAge VALUES (?, ?, ?, ?, ?, ?, ?, ?)"
        c.execute(sql, (popid, name, value, self.biosce, szgroup, age, period, node))

        self.__db.commit()

    def insert_vessel(self, vessel_name):
        c = self.__db.cursor()
        sql = "INSERT INTO VesselsSpe(VesselName, fleetsce) " \
              "VALUES (?, ?)"
        c.execute(sql, (vessel_name, self.fleetsce))
        self.__db.commit()

    def insert_vessel_parameter(self, vessel_name, parameter_name, opt1, opt2, period, value):
        c = self.__db.cursor()
        sql = "INSERT INTO VesselsParameters(VesselName, Parameter, Opt1, Opt2, Period, Value) " \
              "VALUES (?, ?, ?, ?, ?, ?)"
        c.execute(sql, (vessel_name, parameter_name, opt1, opt2, period, value))
        self.__db.commit()

    def insert_config_entry(self, parameter, value):
        c = self.__db.cursor()

        sql = "INSERT INTO Config VALUES (?, ?)"
        c.execute(sql, (parameter, value))

        self.__db.commit()

    def insert_scenario_config_entry(self, parameter, value):
        c = self.__db.cursor()

        sql = "INSERT INTO ScenarioConfig VALUES (?, ?, ?)"
        c.execute(sql, (self.__current_scenario, parameter, value))

        self.__db.commit()

    def create_nodes(self, nodes):
        c = self.db.cursor()

        sql = "INSERT INTO Nodes(id,x,y,hidx,graphsce) VALUES (?, ?, ?, ?, ?)"

        # noinspection PyShadowingBuiltins
        for id, cols in enumerate(nodes):
            c.execute(sql, (id, *cols, self.graphsce))

        self.db.commit()

    def create_edges(self, edges):
        c = self.db.cursor()

        sql = "INSERT INTO Edges VALUES (?, ?, ?, ?, ?)"

        # noinspection PyShadowingBuiltins
        for id, cols in enumerate(edges):
            c.execute(sql, (id, *cols, self.graphsce))

        self.db.commit()

    def __create_biosce(self):
        c = self.db.cursor()

        sql = "INSERT INTO BioSce VALUES (?)"
        c.execute(sql, (self.biosce,))

        self.db.commit()

    def __create_graphsce(self):
        c = self.db.cursor()

        sql = "INSERT INTO GraphSce VALUES (?)"
        c.execute(sql, (self.graphsce,))

        self.db.commit()

    def __create_fleetsce(self):
        c = self.db.cursor()

        sql = "INSERT INTO FleetSce VALUES (?)"
        c.execute(sql, (self.fleetsce,))

        self.db.commit()

    def set_param_in_table(self, table, field, fieldId, fieldSce, values):
        c = self.db.cursor()

        sql = "UPDATE {0} SET {1} = ? WHERE {2} = ? AND {3} = ?".format(table, field, fieldId, fieldSce)

        for value, id, sce in values:
            c.execute(sql, (value, id, sce))

        self.db.commit()
