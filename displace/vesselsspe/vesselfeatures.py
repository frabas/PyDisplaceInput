import csv
import os

from displace.importer import Importer

from ..db.VesselsTable import VesselsTable

class VesselFeatures(Importer):
    def __init__(self):
        super().__init__("vesselsspe_{name}/vesselsspe_economic_features.dat")

    def import_file(self, db):
        print("loading {}".format(os.path.abspath(self.path)))

        with open(self.path) as file:
            rows = tuple(csv.reader(file, delimiter="|"))

        db.prepare_sql(VesselsTable.prepare_insert(VesselsTable.FIELD_NAME,
                       VesselsTable.FIELD_PARAM,
                       VesselsTable.FIELD_OPT1,
                       VesselsTable.FIELD_VALUE
                       ))

        for row in rows:
            vessel_name = row[0]
            db.insert_vessel(vessel_name)
            for i,feature in enumerate(row[1:]):
                db.execute(vessel_name, "feature", i+1, feature)

        db.commit()