import csv
import glob
import os
import re

from displace.importer import Importer


class StaticAvaiFull(Importer):
    def __init__(self):
        super(StaticAvaiFull, self).__init__(
            "popsspe_{name}/static_avai/*spe_full_avai_szgroup_nodes_semester*.dat"
        )

        self.__re = re.compile(".*([0-9])spe_full_avai_szgroup_nodes_semester([0-9]).dat")

    def import_file(self, db):
        files = glob.glob(self.path)

        db.prepare_insert_population_parameter_with_szgroup_and_age()

        for file in files:
            m = self.__re.match(file)

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
                db.insert_population_parameter_with_szgroup_and_age(popid, "static_avai", value, szgroup=size_group,
                                                                    period=semester, node=nodeid)
                size_group += 1
                oldnode_id = nodeid

        db.commit_insert_population_parameter_with_szgroup_and_age()



class StaticAvaiFull(Importer):
    def __init__(self):
        super(StaticAvaiFull, self).__init__(
            "popsspe_{name}/static_avai/*spe_full_avai_szgroup_nodes_semester*.dat"
        )

        self.__re = re.compile(".*([0-9])spe_full_avai_szgroup_nodes_semester([0-9]).dat")

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
                db.insert_population_parameter_with_szgroup_and_age(popid, "static_avai", value, szgroup=size_group,
                                                                    period=semester, node=nodeid)
                size_group += 1
                oldnode_id = nodeid

        db.commit_insert_population_parameter_with_szgroup_and_age()
