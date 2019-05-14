import os

from displace.database import Database
from displace.importer import Importer
from displace.utils import stepped_grouper


class CoordsNodes(Importer):
    def __init__(self):
        super().__init__("graphsspe/coord{biosce}.dat")

    def import_file(self, db: Database):
        print("loading {}".format(os.path.abspath("graphsspe/coord.dat")))

        with open(self.path) as file:
            # strip whitespace from all lines and remove empty ones
            lines = tuple(filter(None, map(str.strip, file.readlines())))

            if len(lines) % 3:
                ValueError(f"File {self.path} has illegal format")

            entries = stepped_grouper(lines, 3, len(lines) // 3)

            db.create_nodes(entries)
