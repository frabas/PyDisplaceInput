import csv
import os

from displace.importer import Importer
from ..db.fishfarms_table import FishfarmsTable


class FishfarmFeaturesImporter(Importer):
    def do_import(self, db, path=None, quarter=None):
        if path is None:
            path = self.path
        print("loading {}".format(os.path.abspath(path)))

        with open(path) as file:
            rows = tuple(csv.reader(file, delimiter="|"))

        db.prepare_sql(FishfarmsTable.prepare_insert(FishfarmsTable.FIELD_NAME,
                                                   FishfarmsTable.FIELD_PARAM,
                                                   FishfarmsTable.FIELD_OPT1,
                                                   FishfarmsTable.FIELD_VALUE,
                                                   FishfarmsTable.FIELD_PERIOD
                                                   ))

        for row in rows:
            fishfarm_name = row[0]
            self.insert_fishfarm(db, fishfarm_name)
            for i, feature in enumerate(row[1:]):
                db.execute(fishfarm_name, self.feature_name, i + 1, feature, quarter)

        db.commit()

    def insert_fishfarm(self, db, fishfarm_name):
        pass


class FishfarmFeatures(FishfarmFeaturesImporter):
    def __init__(self):
        self.feature_name = "feature"
        super().__init__("fishfarmsspe_{name}/fishfarmsspe_features.dat")

    def import_file(self, db):
        self.do_import(db)

    def insert_fishfarm(self, db, fishfarm_name):
        db.insert_fishfarm(fishfarm_name)
