import csv
import os

from displace.importer import Importer

class SpeDeltaHab(Importer):
    def __init__(self):
        super(SpeDeltaHab, self).__init__(
            "benthosspe_{name}/habitat_deltas_per_pop.dat"
        )

    def import_file(self, db):

        with open(self.path) as f:
            rows = tuple(csv.reader(f, delimiter=" "))

        print("loading {}".format(os.path.abspath(self.path)))

        pop_id=0
        oldlandscape_id=-1
        for landscape_id, value in rows[1:]:
            if(oldlandscape_id!=landscape_id):
                pop_id =0
            db.insert_population_parameter(pop_id, "DeltaHab", value, landscape=landscape_id)
            pop_id +=1
            oldlandscape_id=landscape_id