import csv
import os

from displace.importer import Importer

class SpeRelativeStability(Importer):
    def __init__(self):
        super(SpeRelativeStability, self).__init__(
            "popsspe_{name}/{{popid}}ctrysspe_relative_stability_semester{{semester}}.dat"
        )

    def import_file(self, db):
        for popid in db.find_all_populations_ids():
            for semester in 1, 2:
                path = self.path.format(popid=popid, semester=semester)

                print("loading {}".format(os.path.abspath(path)))

                with open(path) as file:
                    rows = tuple(csv.reader(file, delimiter=" "))

                for ctry, stab in rows[1:]:
                    db.insert_population_parameter(popid, "ctrysspe_relative_stability", stab, country=ctry)
