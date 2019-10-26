import csv
import os

from displace.importer import Importer
from ..db.vessels_table import VesselsTable


class VesselFeaturesImporter(Importer):
    def do_import(self, db, path=None, quarter=None):
        if path is None:
            path = self.path
        print("loading {}".format(os.path.abspath(path)))

        with open(path) as file:
            rows = tuple(csv.reader(file, delimiter="|"))

        db.prepare_sql(VesselsTable.prepare_insert(VesselsTable.FIELD_NAME,
                                                   VesselsTable.FIELD_PARAM,
                                                   VesselsTable.FIELD_OPT1,
                                                   VesselsTable.FIELD_VALUE,
                                                   VesselsTable.FIELD_PERIOD
                                                   ))

        for row in rows:
            vessel_name = row[0]
            self.insert_vessel(db, vessel_name)
            for i, feature in enumerate(row[1:]):
                db.execute(vessel_name, self.feature_name, i + 1, feature, quarter)

        db.commit()

    def insert_vessel(self, db, vessel_name):
        pass


class VesselFeatures(VesselFeaturesImporter):
    def __init__(self):
        self.feature_name = "feature"
        super().__init__("vesselsspe_{name}/vesselsspe_features_quarter{{quarter}}.dat")

    def import_file(self, db):
        for quarter in 1, 2, 3, 4:
            path = self.path.format(quarter=quarter)
            self.do_import(db, quarter=quarter, path=path)


class VesselEconomicFeatures(VesselFeaturesImporter):
    def __init__(self):
        self.feature_name = "economic_feature"
        super().__init__("vesselsspe_{name}/vesselsspe_economic_features.dat")

    def insert_vessel(self, db, vessel_name):
        db.insert_vessel(vessel_name)

    def import_file(self, db):
        self.do_import(db)
