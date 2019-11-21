import csv
import glob
import os
import re

from displace.importer import Importer

class BenthosMeanWeight(Importer):
    def __init__(self):
        super(BenthosMeanWeight, self).__init__(
            "benthosspe_{name}/meanw_funcgr_per_landscape.dat"
        )


    def import_file(self, db):
        print("loading {}".format(os.path.abspath(self.path)))

        with open(self.path) as f:
            rows = tuple(csv.reader(f, delimiter=" "))

        db.prepare_insert_benthos_parameter_with_funcgrp()

        funcgrp_id = 0
        oldlandscape_id = -1
        for landscape_id, value in rows[1:]:
                if (oldlandscape_id != landscape_id):
                    funcgrp_id = 0
                db.insert_benthos_parameter_with_funcgrp(landscape_id, "MeanWeight", value,
                                                                    period=None, funcgroup=funcgrp_id)
                funcgrp_id += 1
                oldlandscape_id = landscape_id

        db.commit_insert_benthos_parameter_with_funcgrp()


