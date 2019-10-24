import csv
import os

from displace.importer import Importer


class VesselHarbours(Importer):
    def __init__(self):
        super().__init__("vesselsspe_{name}/vesselsspe_harbours_quarter{{quarter}}.dat")

    def import_file(self, db):
        for quarter in 1, 2, 3, 4:
            path = self.path.format(quarter=quarter)

            print("loading {}".format(os.path.abspath(path)))

            with open(path) as file:
                rows = tuple(csv.reader(file, delimiter=" "))

            for vesselname, value in rows[1:]:
                db.insert_vessel_parameter(vesselname, "harbourNode", opt1=None, opt2=None, period=quarter, value=value)
