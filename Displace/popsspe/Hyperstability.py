import csv
import os

from Displace.Importer import Importer


class Hyperstability(Importer):
    def __init__(self):
        super().__init__("popsspe_{}/hyperstability_param.dat")

    def importFile(self, db):
        print("loading {}".format(os.path.abspath("popsspe/hyperstability_param.dat")))
        with open(self.path) as file:
            reader = csv.DictReader(file, delimiter=' ')
            for row in reader:
                db.insertPopulationParameter(row["stock"], "hyperstability_param",
                                             row["hyperstability_param"])
