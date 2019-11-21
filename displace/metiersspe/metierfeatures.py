import csv
import os

from displace.importer import Importer
from ..db.metiers_table import MetiersTable



class MetierFeaturesImporter(Importer):
    def do_import(self, db, path=None, quarter=None):
        if path is None:
            path = self.path
        print("loading {}".format(os.path.abspath(path)))

        with open(path) as file:
            rows = tuple(csv.reader(file, delimiter=" "))

        db.prepare_sql(MetiersTable.prepare_insert(MetiersTable.FIELD_NAME,
                                                   MetiersTable.FIELD_PARAM,
                                                   MetiersTable.FIELD_OPT1,
                                                   MetiersTable.FIELD_VALUE,
                                                   MetiersTable.FIELD_PERIOD
                                                   ))

        for row in rows:
            metier_name = row[0]
            metier_id= row[1]
            self.insert_metier(db, metier_name, metier_id=metier_id)
            for i, feature in enumerate(row[2:]):
                db.execute(metier_name, self.feature_name, i + 1, feature, quarter)

        db.commit()

    def insert_metier(self, db, metier_name, metier_id=None):
        pass


class MetierFeatures(MetierFeaturesImporter):
    def __init__(self):
        self.feature_name = "metiers_feature"
        super().__init__("metiersspe_{name}/combined_met_names.txt")

    def insert_metier(self, db, metier_name, metier_id):
        db.insert_metier(metier_name, metier_id)

    def import_file(self, db):
        self.do_import(db)
