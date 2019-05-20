import csv
import os

from displace.importer import Importer


class Hyperstability(Importer):
    def __init__(self):
        super().__init__("popsspe_{name}/hyperstability_param.dat")

    def import_file(self, db):
        print("loading {}".format(os.path.abspath(self.path)))
        with open(self.path) as file:
            rows = tuple(csv.reader(file, delimiter=" "))

            for stock, hs_param in rows[1:]:
                db.insert_population_parameter(stock, "hyperstability_param", hs_param)
