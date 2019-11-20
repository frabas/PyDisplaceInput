import csv
import os

from displace.importer import Importer
from ..db.harbours_table import HarboursTable


class HarbourFeaturesImporter(Importer):
    def do_import(self, db, path=None, quarter=None):
        if path is None:
            path = self.path
        print("loading {}".format(os.path.abspath(path)))

        with open(path) as file:
            rows = tuple(csv.reader(file, delimiter="|"))

        db.prepare_sql(HarboursTable.prepare_insert(HarboursTable.FIELD_NAME,
                                                   HarboursTable.FIELD_PARAM,
                                                   HarboursTable.FIELD_OPT1,
                                                   HarboursTable.FIELD_VALUE,
                                                   HarboursTable.FIELD_PERIOD
                                                   ))

        for row in rows:
            harbour_name = row[0]
            self.insert_harbour(db, harbour_name)
            for i, feature in enumerate(row[1:]):
                db.execute(harbour_name, self.feature_name, i + 1, feature, quarter)

        db.commit()

    def insert_harbour(self, db, harbour_name):
        pass


class HarbourFeatures(HarbourFeaturesImporter):
    def __init__(self):
        self.feature_name = "feature"
        super().__init__("harboursspe_{name}/names_harbours.dat")

    def import_file(self, db):
        self.do_import(db)

    def insert_harbour(self, db, harbour_name):
        db.insert_harbour(harbour_name)
