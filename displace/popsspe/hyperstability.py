import csv
import os

from displace.importer import Importer


class Hyperstability(Importer):
    def __init__(self):
        super().__init__("popsspe_{biosce_name}/hyperstability_param.dat")

    def import_file(self, db):
        print("loading {}".format(os.path.abspath("popsspe/hyperstability_param.dat")))
        with open(self.path) as file:
            reader = csv.DictReader(file, delimiter=' ')
            for row in reader:
                db.insert_population_parameter(row["stock"], "hyperstability_param",
                                               row["hyperstability_param"])
