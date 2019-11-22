import csv
import glob
import os
import re

from displace.importer import Importer


class MetierSelOgive(Importer):
    def __init__(self):
        super(MetierSelOgive, self).__init__(
            "metiersspe_{name}/*metier_selectivity_per_stock_ogives_fleetsce*.dat"
        )

        self.__re = re.compile(".*([0-9]+)metier_selectivity_per_stock_ogives_fleetsce([0-9]).dat")

    def import_file(self, db):
        files = glob.glob(self.path)

        db.prepare_insert_metier_parameter_with_species_szgroup()

        for file in files:
            m = self.__re.match(file)
            if m is None:
                print("Skipping file: {}".format(file))
                continue

            metierid = m.group(1)
            fleetsce = m.group(2)
            period = None

            print("loading {}".format(os.path.abspath(file)))


            with open(file) as f:
               for species, vals in enumerate(csv.reader(f, delimiter=" ")):
                  for szgroup, value in enumerate(vals):
                      db.insert_metier_parameter_with_species_szgroup(
                                    metierid, "SelOgive", value, fleetsce, species, szgroup, period)

            # the delimiter type can be an issue here for some existing Displace apps

        db.commit_insert_metier_parameter_with_species_szgroup()



class MetierSelOgiveOth(Importer):
    def __init__(self):
        super(MetierSelOgiveOth, self).__init__(
            "metiersspe_{name}/metier_selectivity_per_stock_ogives_fleetsce*_for_oth_land.dat"
        )

        self.__re = re.compile(".*metier_selectivity_per_stock_ogives_fleetsce([0-9])_for_oth_land.dat")

    def import_file(self, db):
        files = glob.glob(self.path)

        db.prepare_insert_metier_parameter_with_species_szgroup()

        for file in files:
            m = self.__re.match(file)
            if m is None:
                print("Skipping file: {}".format(file))
                continue

            fleetsce = m.group(1)
            period = None

            print("loading {}".format(os.path.abspath(file)))


            with open(file) as f:
               for species, vals in enumerate(csv.reader(f, delimiter=" ")):
                  for szgroup, value in enumerate(vals):
                      db.insert_metier_parameter_with_species_szgroup(
                                    1000, "SelOgiveOth", value, fleetsce, species, szgroup, period)

            # the delimiter type can be an issue here for some existing Displace apps

        db.commit_insert_metier_parameter_with_species_szgroup()

