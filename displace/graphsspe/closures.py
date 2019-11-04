import csv
import os

from displace.db.closures_table import ClosuresTable
from displace.importer import Importer


class ClosuresImporter(Importer):
    def __init__(self, path, keyword):
        super().__init__(path)
        self.keyword = keyword

    def import_file(self, db):
        db.prepare_sql(ClosuresTable.prepare_insert(ClosuresTable.FIELD_CLOSURESCE,
                                                    ClosuresTable.FIELD_ID,
                                                    ClosuresTable.FIELD_NODE,
                                                    ClosuresTable.FIELD_PERIOD,
                                                    ClosuresTable.FIELD_TYPE,
                                                    ClosuresTable.FIELD_OPT,
                                                    ClosuresTable.FIELD_VALUE
                                                    ))

        """
        closures = db.get_scenario_config_entry("metier_closures")
        if closures == "":
            return
        
        closures = closures.split(" ")

        for closure in closures:
            pass
        """
        closure = db.graphsce

        for month in range(1, 13):
            path = self.path.format(sce=closure, month=month)
            print("loading {}".format(os.path.abspath(path)))

            with open(path) as f:
                rows = tuple(csv.reader(f, delimiter=" "))

            for row in rows:
                if len(row) < 3:
                    continue
                db.execute(closure, row[0], row[2], month, self.keyword,
                           row[1], " ".join(row[3:])
                           )

        db.commit()


class ClosuresMetier(ClosuresImporter):
    def __init__(self):
        super().__init__("graphsspe/metier_closure_a_graph{{sce}}_month{{month}}.dat", "metier")


class ClosuresVSize(ClosuresImporter):
    def __init__(self):
        super().__init__("graphsspe/vsize_closure_a_graph{{sce}}_month{{month}}.dat", "vsize")
