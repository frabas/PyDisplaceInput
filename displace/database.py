import os
import sqlite3
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

    def prepare_sql(self, sqlStatement):
        self.sql = sqlStatement
        self.cur = self.__db.cursor()

    def execute(self, *params):
        try:
            self.cur.execute(self.sql, params)
        except sqlite3.IntegrityError as x:
            print("On executing {} with Params {}:".format(self.sql, params))
            raise

    def commit(self):
        self.__db.commit()
        self.sql = None
        self.cur = None

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

    def prepare_insert_population_parameter_with_szgroup_and_age(self):
        self.prepare_sql("INSERT INTO PopulationParametersWithSizeGroupAndAge VALUES (?, ?, ?, ?, ?, ?, ?, ?)")

    def insert_population_parameter_with_szgroup_and_age(self, popid, name, value, szgroup=None, age=None, period=None, node=None):
        self.cur.execute(self.sql, (popid, name, value, self.biosce, szgroup, age, period, node))

    def commit_insert_population_parameter_with_szgroup_and_age(self):
        self.commit()

    def prepare_insert_harbour_parameter_with_species_and_marketcat(self):
        self.prepare_sql("INSERT INTO HarbourParametersWithSpeciesAndMarketCat VALUES (?, ?, ?, ?, ?, ?)")

    def insert_harbour_parameter_with_species_and_marketcat(self, nodeid, parameter, value, marketcat=None, period=None, species=None):
        self.cur.execute(self.sql, (nodeid, parameter, value, marketcat,  period, species))

    def commit_harbour_parameter_with_species_and_marketcat(self):
        self.commit()

    def prepare_insert_harbour_parameter_with_vesselsize(self):
        self.prepare_sql("INSERT INTO HarbourParametersWithVesselSize VALUES (?, ?, ?, ?, ?)")

    def insert_harbour_parameter_with_vesselsize(self, nodeid, parameter, value, period=None, vesselsize=None):
        self.cur.execute(self.sql, (nodeid, parameter, value,  period, vesselsize))

    def commit_harbour_parameter_with_vesselsize(self):
        self.commit()

    def insert_harbour(self, node_id, harbour_name):
        c = self.__db.cursor()
        sql = "INSERT INTO HarboursSpe(node_id, HarbourName, graphsce) " \
              "VALUES (?, ?, ?)"
        c.execute(sql, (node_id, harbour_name, self.graphsce))
        self.__db.commit()

    def insert_harbour_parameter(self, node_id, parameter_name, opt1, opt2, period, value):
        c = self.__db.cursor()
        sql = "INSERT INTO HarboursParameters(NodeId, Parameter, Opt1, Opt2, Period, Value) " \
              "VALUES (?, ?, ?, ?, ?, ?)"
        c.execute(sql, (node_id, parameter_name, opt1, opt2, period, value))
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

    def insert_fishfarm(self, fishfarm_name):
        c = self.__db.cursor()
        sql = "INSERT INTO FishfarmsSpe(FishfarmName) " \
              "VALUES (?)"
        c.execute(sql, (fishfarm_name,))
        self.__db.commit()

    def insert_fishfarm_parameter(self, fishfarm_name, parameter_name, opt1, opt2, period, value):
        c = self.__db.cursor()
        sql = "INSERT INTO FishfarmsParameters(FishfarmName, Parameter, Opt1, Opt2, Period, Value) " \
              "VALUES (?, ?, ?, ?, ?, ?)"
        c.execute(sql, (fishfarm_name, parameter_name, opt1, opt2, period, value))
        self.__db.commit()

    def insert_ship(self, ship_name):
        c = self.__db.cursor()
        sql = "INSERT INTO ShipsSpe(ShipName) " \
              "VALUES (?)"
        c.execute(sql, (ship_name,))
        self.__db.commit()

    def insert_ship_parameter(self, ship_name, parameter_name, opt1, opt2, period, value):
        c = self.__db.cursor()
        sql = "INSERT INTO ShipsParameters(ShipName, Parameter, Opt1, Opt2, Period, Value) " \
              "VALUES (?, ?, ?, ?, ?, ?)"
        c.execute(sql, (ship_name, parameter_name, opt1, opt2, period, value))
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

    def get_scenario_config_entry(self, parameter):
        c = self.__db.cursor()

        sql = "SELECT value FROM ScenarioConfig WHERE sce=? AND param=?"
        c.execute(sql, (self.__current_scenario, parameter))
        row = c.fetchall()
        if len(row) > 0:
            return row[0]
        return ""
    
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
