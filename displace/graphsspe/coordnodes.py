from displace.database import Database
from displace.importer import NSplitsFileImporter


class CoordNodes(NSplitsFileImporter):
    def __init__(self):
        super().__init__("graphsspe/coord{biosce}.dat", 3, Database.create_nodes)
