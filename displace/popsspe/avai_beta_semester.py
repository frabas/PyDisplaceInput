import csv
import glob
import os
import re

from displace.importer import Importer


class AvaiBetaSemester(Importer):
    def __init__(self):
        super(AvaiBetaSemester, self).__init__(
            "popsspe_{name}/avai*_betas_semester*.dat"
        )

        self.__re = re.compile(".*avai([0-9]+)_betas_semester([0-9]).dat")

    def import_file(self, db):
        files = glob.glob(self.path)

        for file in files:
            m = self.__re.match(file)

            size_group = m.group(1)
            semester = m.group(2)

            print("loading {}".format(os.path.abspath(file)))
            with open(file) as f:
                rows = tuple(csv.reader(f, delimiter=" "))

            for popid, value in rows[1:]:
                db.insert_population_parameter_with_szgroup_and_age(popid, "beta", value, szgroup=size_group, period=semester)
