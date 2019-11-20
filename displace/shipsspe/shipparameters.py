import csv
import os

from displace.db.ships_table import ShipsTable
from displace.importer import Importer


class ShipLanesLat(Importer):
    def __init__(self):
        super().__init__("shipsspe_{name}/shipsspe_lanes_lat.dat")

    def import_file(self, db):
        db.prepare_sql(ShipsTable.prepare_insert(ShipsTable.FIELD_NAME,
                                                   ShipsTable.FIELD_PARAM,
                                                   ShipsTable.FIELD_OPT1,
                                                   ShipsTable.FIELD_VALUE
                                                   ))

        print("loading {}".format(os.path.abspath(self.path)))
        with open(self.path) as f:
            rows = tuple(csv.reader(f, delimiter=" "))

        for row in rows[1:]:
            if len(row) < 2:
                continue
            opt1 = row[0]
            value = row[1]
            db.execute("**LanesLat**", "LanesLat", opt1, value)

        db.commit()


class ShipLanesLon(Importer):
    def __init__(self):
        super().__init__("shipsspe_{name}/shipsspe_lanes_lon.dat")

    def import_file(self, db):
        db.prepare_sql(ShipsTable.prepare_insert(ShipsTable.FIELD_NAME,
                                                   ShipsTable.FIELD_PARAM,
                                                   ShipsTable.FIELD_OPT1,
                                                   ShipsTable.FIELD_VALUE
                                                   ))

        print("loading {}".format(os.path.abspath(self.path)))
        with open(self.path) as f:
            rows = tuple(csv.reader(f, delimiter=" "))

        for row in rows[1:]:
            if len(row) < 2:
                continue
            opt1 = row[0]
            value = row[1]
            db.execute("**LanesLon**", "LanesLon", opt1, value)

        db.commit()
