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


class NodesMarineLandscape(NSplitsFileImporter):
    def __init__(self):
        super().__init__("graphsspe/coord{graphsce}_with_landscape.dat", 1, self._import)

    def _import(self, db, linesIt):
        lines = [x[0] for x in linesIt]
        values = list(zip(lines, range(0, len(lines)), [db.graphsce] * len(lines)))
        db.set_param_in_table("Nodes", "landscape", "id", "graphsce", values)


class NodesWind(NSplitsFileImporter):
    def __init__(self):
        super().__init__("graphsspe/coord{graphsce}_with_wind.dat", 1, self._import)

    def _import(self, db, linesIt):
        lines = [x[0] for x in linesIt]
        values = list(zip(lines, range(0, len(lines)), [db.graphsce] * len(lines)))
        db.set_param_in_table("Nodes", "wind", "id", "graphsce", values)


class NodesSalinity(NSplitsFileImporter):
    def __init__(self):
        super().__init__("graphsspe/coord{graphsce}_with_salinity.dat", 1, self._import)

    def _import(self, db, linesIt):
        lines = [x[0] for x in linesIt]
        values = list(zip(lines, range(0, len(lines)), [db.graphsce] * len(lines)))
        db.set_param_in_table("Nodes", "salinity", "id", "graphsce", values)


class NodesSST(NSplitsFileImporter):
    def __init__(self):
        super().__init__("graphsspe/coord{graphsce}_with_sst.dat", 1, self._import)

    def _import(self, db, linesIt):
        lines = [x[0] for x in linesIt]
        values = list(zip(lines, range(0, len(lines)), [db.graphsce] * len(lines)))
        db.set_param_in_table("Nodes", "sst", "id", "graphsce", values)


class NodesNitrogen(NSplitsFileImporter):
    def __init__(self):
        super().__init__("graphsspe/coord{graphsce}_with_nitrogen.dat", 1, self._import)

    def _import(self, db, linesIt):
        lines = [x[0] for x in linesIt]
        values = list(zip(lines, range(0, len(lines)), [db.graphsce] * len(lines)))
        db.set_param_in_table("Nodes", "nitrogen", "id", "graphsce", values)


class NodesPhosphorus(NSplitsFileImporter):
    def __init__(self):
        super().__init__("graphsspe/coord{graphsce}_with_phosphorus.dat", 1, self._import)

    def _import(self, db, linesIt):
        lines = [x[0] for x in linesIt]
        values = list(zip(lines, range(0, len(lines)), [db.graphsce] * len(lines)))
        db.set_param_in_table("Nodes", "phosphorus", "id", "graphsce", values)


class NodesOxygen(NSplitsFileImporter):
    def __init__(self):
        super().__init__("graphsspe/coord{graphsce}_with_oxygen.dat", 1, self._import)

    def _import(self, db, linesIt):
        lines = [x[0] for x in linesIt]
        values = list(zip(lines, range(0, len(lines)), [db.graphsce] * len(lines)))
        db.set_param_in_table("Nodes", "oxygen", "id", "graphsce", values)


class NodesCarbon(NSplitsFileImporter):
    def __init__(self):
        super().__init__("graphsspe/coord{graphsce}_with_dissolvedcarbon.dat", 1, self._import)

    def _import(self, db, linesIt):
        lines = [x[0] for x in linesIt]
        values = list(zip(lines, range(0, len(lines)), [db.graphsce] * len(lines)))
        db.set_param_in_table("Nodes", "carbon", "id", "graphsce", values)


class NodesBathymetry(NSplitsFileImporter):
    def __init__(self):
        super().__init__("graphsspe/coord{graphsce}_with_bathymetry.dat", 1, self._import)

    def _import(self, db, linesIt):
        lines = [x[0] for x in linesIt]
        values = list(zip(lines, range(0, len(lines)), [db.graphsce] * len(lines)))
        db.set_param_in_table("Nodes", "bathymetry", "id", "graphsce", values)


class NodesShipping(NSplitsFileImporter):
    def __init__(self):
        super().__init__("graphsspe/coord{graphsce}_with_shippingdensity.dat", 1, self._import)

    def _import(self, db, linesIt):
        lines = [x[0] for x in linesIt]
        values = list(zip(lines, range(0, len(lines)), [db.graphsce] * len(lines)))
        db.set_param_in_table("Nodes", "shipping", "id", "graphsce", values)


class NodesSilt(NSplitsFileImporter):
    def __init__(self):
        super().__init__("graphsspe/coord{graphsce}_with_siltfraction.dat", 1, self._import)

    def _import(self, db, linesIt):
        lines = [x[0] for x in linesIt]
        values = list(zip(lines, range(0, len(lines)), [db.graphsce] * len(lines)))
        db.set_param_in_table("Nodes", "silt", "id", "graphsce", values)


class NodesBenthosBio(NSplitsFileImporter):
    def __init__(self):
        super().__init__("graphsspe/coord{graphsce}_with_benthos_total_biomass.dat", 1, self._import)

    def _import(self, db, linesIt):
        lines = [x[0] for x in linesIt]
        values = list(zip(lines, range(0, len(lines)), [db.graphsce] * len(lines)))
        db.set_param_in_table("Nodes", "benthosbio", "id", "graphsce", values)


class NodesBenthosNum(NSplitsFileImporter):
    def __init__(self):
        super().__init__("graphsspe/coord{graphsce}_with_benthos_total_number.dat", 1, self._import)

    def _import(self, db, linesIt):
        lines = [x[0] for x in linesIt]
        values = list(zip(lines, range(0, len(lines)), [db.graphsce] * len(lines)))
        db.set_param_in_table("Nodes", "benthosnum", "id", "graphsce", values)
