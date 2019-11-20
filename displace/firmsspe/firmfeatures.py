import csv
import os

from displace.importer import Importer
from ..db.firms_table import FirmsTable


class FirmFeaturesImporter(Importer):
    def do_import(self, db, path=None, quarter=None):
        if path is None:
            path = self.path
        print("loading {}".format(os.path.abspath(path)))

        with open(path) as file:
            rows = tuple(csv.reader(file, delimiter="|"))

        db.prepare_sql(FirmsTable.prepare_insert(FirmsTable.FIELD_NAME,
                                                   FirmsTable.FIELD_PARAM,
                                                   FirmsTable.FIELD_OPT1,
                                                   FirmsTable.FIELD_VALUE,
                                                   FirmsTable.FIELD_PERIOD
                                                   ))

        for row in rows:
            firm_name = row[0]
            self.insert_firm(db, firm_name)
            for i, feature in enumerate(row[1:]):
                db.execute(firm_name, self.feature_name, i + 1, feature, quarter)

        db.commit()

    def insert_firm(self, db, ship_name):
        pass


class FirmFeatures(FirmFeaturesImporter):
    def __init__(self):
        self.feature_name = "feature"
        super().__init__("firmsspe_{name}/firms_specs.dat")

    def insert_ship(self, db, firm_name):
        db.insert_ship(firm_name)

    def import_file(self, db):
        self.do_import(db)
