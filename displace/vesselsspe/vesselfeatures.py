import csv
import os

from displace.importer import Importer


class VesselFeatures(Importer):
    def __init__(self):
        super().__init__("vesselsspe_{name}/vesselsspe_economic_features.dat")

    def import_file(self, db):
        print("loading {}".format(os.path.abspath(self.path)))

        with open(self.path) as file:
            rows = tuple(csv.reader(file, delimiter="|"))

        for row in rows:
            vessel_name = row[0]
            db.insert_vessel(vessel_name)
            for i,feature in enumerate(row[1:]):
                db.insert_vessel_parameter(vessel_name, "feature", opt1=i+1, opt2=None, period=None, value=feature)
