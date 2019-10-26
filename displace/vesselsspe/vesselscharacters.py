import csv
import glob
import os
import re

from displace.db.vessels_table import VesselsTable
from displace.importer import Importer


class VesselPossibleMetier(Importer):
    def __init__(self):
        super().__init__("vesselsspe_{name}/*_possible_metiers_quarter*.dat")
        self.__re = re.compile("([A-Za-z0-9]+)_possible_metiers_quarter([0-9]).dat")

    def import_file(self, db):
        files = glob.glob(self.path)

        db.prepare_sql(VesselsTable.prepare_insert(VesselsTable.FIELD_NAME,
                                                   VesselsTable.FIELD_PARAM,
                                                   VesselsTable.FIELD_OPT1,
                                                   VesselsTable.FIELD_PERIOD,
                                                   VesselsTable.FIELD_VALUE
                                                   ))
        for file in files:
            m = self.__re.match(os.path.basename(file))
            if m is None:
                continue

            vessel_name = m.group(1)
            quarter = m.group(2)

            print("loading {}".format(os.path.abspath(file)))
            with open(file) as f:
                rows = tuple(csv.reader(f, delimiter=" "))

            for fground, metier in rows[1:]:
                db.execute(vessel_name, "PossibleMetier", fground, quarter, metier)

        db.commit()
