import csv
import os

from displace.db.vessels_table import VesselsTable
from displace.importer import Importer


class VesselPrices(Importer):
    def __init__(self):
        super().__init__("vesselsspe_{name}/fuel_price_per_vessel_size.dat")

    def import_file(self, db):
        db.prepare_sql(VesselsTable.prepare_insert(VesselsTable.FIELD_NAME,
                                                   VesselsTable.FIELD_PARAM,
                                                   VesselsTable.FIELD_OPT1,
                                                   VesselsTable.FIELD_VALUE
                                                   ))

        print("loading {}".format(os.path.abspath(self.path)))
        with open(self.path) as f:
            rows = tuple(csv.reader(f, delimiter=" "))

        for row in rows[1:]:
            if len(row) < 2:
                continue
            opt1 = row[0]
            value = row[1]
            db.execute("**FuelPrice**", "FuelPrice", opt1, value)

        db.commit()
