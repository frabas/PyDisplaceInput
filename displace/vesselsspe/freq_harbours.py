import csv
import os

from displace.importer import Importer
from ..db.vessels_table import VesselsTable


class VesselFreqHarbours(Importer):
    def __init__(self):
        super().__init__("vesselsspe_{name}/vesselsspe_freq_harbours_quarter{{quarter}}.dat")

    def import_file(self, db):

        db.prepare_sql(VesselsTable.prepare_insert(VesselsTable.FIELD_NAME,
                                                   VesselsTable.FIELD_PARAM,
                                                   VesselsTable.FIELD_PERIOD,
                                                   VesselsTable.FIELD_VALUE))

        for quarter in 1, 2, 3, 4:
            path = self.path.format(quarter=quarter)

            print("loading {}".format(os.path.abspath(path)))

            with open(path) as file:
                rows = tuple(csv.reader(file, delimiter=" "))

            for row in rows[1:]:
                if len(row) == 0:
                    continue
            
                db.execute(row[0], "harbourFreq", quarter, row[1])

        db.commit()
