from displace.database import Database
from displace.importer import NSplitsFileImporter


class CoordNodes(NSplitsFileImporter):
    def __init__(self):
        super().__init__("graphsspe/coord{graphsce}.dat", 3, Database.create_nodes)


class NodesCodeArea(NSplitsFileImporter):
    def __init__(self):
        super().__init__("graphsspe/code_area_for_graph{graphsce}_points.dat", 3, self._import)

    def _import(self, db, linesIt):
        lines = [x[2] for x in linesIt]
        values = list(zip(lines, range(0, len(lines)), [db.graphsce] * len(lines)))
        db.set_param_in_table("Nodes", "code_area", "id", "graphsce", values)
