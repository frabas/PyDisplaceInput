import os
import csv
from displace.importer import Importer


class SpeSizeTransitionMatrix(Importer):
    def __init__(self):
        super(SpeSizeTransitionMatrix, self).__init__(
            "popsspe_{name}/{{popid}}spe_size_transition_matrix_biolsce{biosce}.dat"
        )

    def import_file(self, db):
        for popid in db.find_all_populations_ids():
            path = self.path.format(popid=popid)

            print("loading {}".format(os.path.abspath(path)))

            with open(path) as f:
                tm = tuple(csv.reader(f, delimiter=" "))

            db.insert_population_transition_matrix(popid=popid, period=None, values=tm )
