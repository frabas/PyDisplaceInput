import csv
import os

from displace.importer import Importer
from ..db.ships_table import ShipsTable


class ShipFeaturesImporter(Importer):
    def do_import(self, db, path=None, quarter=None):
        if path is None:
            path = self.path
        print("loading {}".format(os.path.abspath(path)))

        with open(path) as file:
            rows = tuple(csv.reader(file, delimiter="|"))

        db.prepare_sql(ShipsTable.prepare_insert(ShipsTable.FIELD_NAME,
                                                   ShipsTable.FIELD_PARAM,
                                                   ShipsTable.FIELD_OPT1,
                                                   ShipsTable.FIELD_VALUE,
                                                   ShipsTable.FIELD_PERIOD
                                                   ))

        for row in rows:
            ship_name = row[0]
            self.insert_ship(db, ship_name)
            for i, feature in enumerate(row[1:]):
                db.execute(ship_name, self.feature_name, i + 1, feature, quarter)

        db.commit()

    def insert_ship(self, db, ship_name):
        pass


class ShipFeatures(ShipFeaturesImporter):
    def __init__(self):
        self.feature_name = "feature"
        super().__init__("shipsspe_{name}/shipsspe_features.dat")

    def insert_ship(self, db, ship_name):
        db.insert_ship(ship_name)

    def import_file(self, db):
        self.do_import(db)
