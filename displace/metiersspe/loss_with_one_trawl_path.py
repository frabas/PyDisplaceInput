import csv
import glob
import os
import re

from displace.importer import Importer


class MetierDepletionOnHab(Importer):
    def __init__(self):
        super(MetierDepletionOnHab, self).__init__(
            "metiersspe_{name}/*loss_after_one_passage_per_landscape_per_func_group.dat"
        )

        self.__re = re.compile(".*([0-9]+)loss_after_one_passage_per_landscape_per_func_group.dat")

    def import_file(self, db):
        files = glob.glob(self.path)

        db.prepare_insert_metier_parameter_with_landscape()

        for file in files:
            m = self.__re.match(file)

            metierid = m.group(1)

            print("loading {}".format(os.path.abspath(file)))
            with open(file) as f:
                rows = tuple(csv.reader(f, delimiter=" "))

            funcgroup = 0
            oldlandscape_id = -1
            for landscape_id, value in rows[1:]:
                if (oldlandscape_id != landscape_id):
                    funcgroup = 0
                db.insert_metier_parameter_with_landscape(metierid, "DepletionOnHab", value, funcgroup=funcgroup,
                                                                    period=None, landscape=landscape_id)
                funcgroup += 1
                oldlandscape_id = landscape_id

        db.commit_insert_metier_parameter_with_landscape()


