import csv
import glob
import os
import re

from displace.importer import Importer


class HarbourFishPrice(Importer):
    def __init__(self):
        super(HarbourFishPrice, self).__init__(
            "harboursspe_{name}/*_quarter*_each_species_per_cat.dat"
        )

        self.__re = re.compile(".*([0-9])_quarter([0-9])_each_species_per_cat.dat")
# TODO: the nodeid is not captured adequately...we would expect the regex for all int to be '^[0-9]+$' ?

    def import_file(self, db):
        files = glob.glob(self.path)

        db.prepare_insert_harbour_parameter_with_species_and_marketcat()

        for file in files:
            m = self.__re.match(file)
            if m is None:
                print("Skipping file: {}".format(file))
                continue

            nodeid = m.group(1)
            quarter = m.group(2)

            print("loading {}".format(os.path.abspath(file)))
            with open(file) as f:
                rows = tuple(csv.reader(f, delimiter=" "))

            market_cat = 0
            oldpop_id = -1
            for popid, value in rows[1:]:
                if (oldpop_id != popid):
                    market_cat = 0
                db.insert_harbour_parameter_with_species_and_marketcat(nodeid,"fishPrice",value, marketcat=market_cat,
                                                                    period=quarter, species=popid)
                market_cat += 1
                oldpop_id = popid

        db.commit_harbour_parameter_with_species_and_marketcat()



