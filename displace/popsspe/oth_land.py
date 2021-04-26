import csv
import glob
import os
import re

from displace.importer import Importer


class OthLand(Importer):
    def __init__(self):
        super(OthLand, self).__init__(
            "popsspe_{name}/*spe_stecf_oth_land_per_month_per_node_month*_fleetsce*.dat"
        )

        self.__re = re.compile(".*([0-9]+)spe_stecf_oth_land_per_month_per_node_month.*([0-9]+)_fleetsce([0-9]).dat")

    def import_file(self, db):
        files = glob.glob(self.path)

        db.prepare_insert_population_parameter_with_szgroup_and_age()

        for file in files:
            m = self.__re.match(file)
            if m is None:
                print("Skipping file: {}".format(file))
                continue

            popid = m.group(1)
            semester = m.group(2)

            print("loading {}".format(os.path.abspath(file)))
            with open(file) as f:
                rows = tuple(csv.reader(f, delimiter=" "))

            size_group = 0
            oldnode_id = -1
            for nodeid, value in rows[1:]:
                if (oldnode_id != nodeid):
                    size_group = 0
                db.insert_population_parameter_with_szgroup_and_age(popid, "oth_land", value, szgroup=size_group,
                                                                    period=semester, node=nodeid)
                size_group += 1
                oldnode_id = nodeid

        db.commit_insert_population_parameter_with_szgroup_and_age()

