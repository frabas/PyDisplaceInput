from displace.database import Database
from displace.importer import NSplitsFileImporter


class GraphEdges(NSplitsFileImporter):
    def __init__(self):
        super(GraphEdges, self).__init__("graphsspe/graph{biosce}.dat", 3, Database.create_edges)
