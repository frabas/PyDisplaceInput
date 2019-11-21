import csv
import glob
import os
import re

from displace.importer import Importer


class HarbourFuelPrice(Importer):
    def __init__(self):
        super(HarbourFuelPrice, self).__init__(
            "harboursspe_{name}/*_quarter*_fuel_price_per_vessel_size.dat"
        )

        self.__re = re.compile(".*(^[0-9]|[1-9][0-9]|[1-9][0-9][0-9]|[1-9][0-9][0-9][0-9]$)_quarter([0-9])_fuel_price_per_vessel_size.dat")

    def import_file(self, db):
        files = glob.glob(self.path)

        db.prepare_insert_harbour_parameter_with_vesselsize()

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

            for popid, value in rows[1:]:
                db.insert_harbour_parameter_with_vesselsize(nodeid,"fuelPrice",value,
                                                                    period=quarter, vesselsize=popid)

        db.commit_harbour_parameter_with_vesselsize()



