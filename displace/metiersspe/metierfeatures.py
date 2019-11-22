import csv
import os

from displace.importer import Importer
from ..db.metiers_table import MetiersTable



class MetierFeaturesImporter(Importer):
    def do_import(self, db, path=None, quarter=None):
        if path is None:
            path = self.path
        print("loading {}".format(os.path.abspath(path)))

        with open(path) as file:
            rows = tuple(csv.reader(file, delimiter=" "))

        db.prepare_sql(MetiersTable.prepare_insert(MetiersTable.FIELD_NAME,
                                                   MetiersTable.FIELD_PARAM,
                                                   MetiersTable.FIELD_OPT1,
                                                   MetiersTable.FIELD_VALUE,
                                                   MetiersTable.FIELD_PERIOD
                                                   ))

        for row in rows:
            metier_name = row[0]
            metier_id= row[1]
            self.insert_metier(db, metier_name, metier_id=metier_id)
            for i, feature in enumerate(row[2:]):
                db.execute(metier_name, self.feature_name, i + 1, feature, quarter)

        db.commit()

    def insert_metier(self, db, metier_name, metier_id=None):
        pass


class MetierFeatures(MetierFeaturesImporter):
    def __init__(self):
        self.feature_name = "metiers_feature"
        super().__init__("metiersspe_{name}/combined_met_names.txt")

    def insert_metier(self, db, metier_name, metier_id):
        db.insert_metier(metier_name, metier_id)

    def import_file(self, db):
        self.do_import(db)



class MetierTargetStock(MetierFeaturesImporter):
    def __init__(self):
        super().__init__("metiersspe_{name}/met_target_names.dat")

    def import_file(self, db):
        db.prepare_sql(MetiersTable.prepare_insert(MetiersTable.FIELD_NAME,
                                                   MetiersTable.FIELD_PARAM,
                                                   MetiersTable.FIELD_VALUE
                                                   ))

        with open(self.path) as file:
            rows = tuple(csv.reader(file, delimiter=" "))

        print("Loading: {}".format(os.path.abspath(self.path)))

        for row in rows[1:]:
            if len(row) < 2:
                continue
            db.execute(row[0], "TargetStock", row[1])
        db.commit()




class MetierSpeedAtFishing(MetierFeaturesImporter):
    def __init__(self):
        super().__init__("metiersspe_{name}/metier_fspeed.dat")

    def import_file(self, db):
        db.prepare_sql(MetiersTable.prepare_insert(MetiersTable.FIELD_NAME,
                                                   MetiersTable.FIELD_PARAM,
                                                   MetiersTable.FIELD_VALUE
                                                   ))

        with open(self.path) as file:
            rows = tuple(csv.reader(file, delimiter=" "))

        print("Loading: {}".format(os.path.abspath(self.path)))

        for row in rows[1:]:
            if len(row) < 2:
                continue
            db.execute(row[0], "SpeedAtFishing", row[1])
        db.commit()


class MetierType(MetierFeaturesImporter):
    def __init__(self):
        super().__init__("metiersspe_{name}/combined_met_types.dat")

    def import_file(self, db):
        db.prepare_sql(MetiersTable.prepare_insert(MetiersTable.FIELD_NAME,
                                                   MetiersTable.FIELD_PARAM,
                                                   MetiersTable.FIELD_VALUE
                                                   ))

        with open(self.path) as file:
            rows = tuple(csv.reader(file, delimiter=" "))

        print("Loading: {}".format(os.path.abspath(self.path)))

        for row in rows[1:]:
            if len(row) < 2:
                continue
            db.execute(row[0], "MetierType", row[1])
        db.commit()


class MetierGearWidthModel(MetierFeaturesImporter):
    def __init__(self):
        super().__init__("metiersspe_{name}/metier_gear_widths_model_type.dat")

    def import_file(self, db):
        db.prepare_sql(MetiersTable.prepare_insert(MetiersTable.FIELD_NAME,
                                                   MetiersTable.FIELD_PARAM,
                                                   MetiersTable.FIELD_VALUE
                                                   ))

        with open(self.path) as file:
            rows = tuple(csv.reader(file, delimiter=" "))

        print("Loading: {}".format(os.path.abspath(self.path)))

        for row in rows[1:]:
            if len(row) < 2:
                continue
            db.execute(row[0], "GearWidthModel", row[1])
        db.commit()

class MetierGearWidthA(MetierFeaturesImporter):
    def __init__(self):
        super().__init__("metiersspe_{name}/metier_gear_widths_param_a.dat")

    def import_file(self, db):
        db.prepare_sql(MetiersTable.prepare_insert(MetiersTable.FIELD_NAME,
                                                   MetiersTable.FIELD_PARAM,
                                                   MetiersTable.FIELD_VALUE
                                                   ))

        with open(self.path) as file:
            rows = tuple(csv.reader(file, delimiter=" "))

        print("Loading: {}".format(os.path.abspath(self.path)))

        for row in rows[1:]:
            if len(row) < 2:
                continue
            db.execute(row[0], "GearWidthA", row[1])
        db.commit()

class MetierGearWidthB(MetierFeaturesImporter):
    def __init__(self):
        super().__init__("metiersspe_{name}/metier_gear_widths_param_b.dat")

    def import_file(self, db):
        db.prepare_sql(MetiersTable.prepare_insert(MetiersTable.FIELD_NAME,
                                                   MetiersTable.FIELD_PARAM,
                                                   MetiersTable.FIELD_VALUE
                                                   ))

        with open(self.path) as file:
            rows = tuple(csv.reader(file, delimiter=" "))

        print("Loading: {}".format(os.path.abspath(self.path)))

        for row in rows[1:]:
            if len(row) < 2:
                continue
            db.execute(row[0], "GearWidthB", row[1])
        db.commit()

class MetierSuitableBottomType(MetierFeaturesImporter):
    def __init__(self):
        super().__init__("metiersspe_{name}/metier_suitable_seabottomtypes.dat")

    def import_file(self, db):
        db.prepare_sql(MetiersTable.prepare_insert(MetiersTable.FIELD_NAME,
                                                   MetiersTable.FIELD_PARAM,
                                                   MetiersTable.FIELD_VALUE
                                                   ))

        with open(self.path) as file:
            rows = tuple(csv.reader(file, delimiter=" "))

        print("Loading: {}".format(os.path.abspath(self.path)))

        for row in rows[1:]:
            if len(row) < 2:
                continue
            db.execute(row[0], "BottomType", row[1])
        db.commit()


class MetierRevenueCompleteness(MetierFeaturesImporter):
    def __init__(self):
        super().__init__("metiersspe_{name}/percent_revenue_completenesses.dat")

    def import_file(self, db):
        db.prepare_sql(MetiersTable.prepare_insert(MetiersTable.FIELD_NAME,
                                                   MetiersTable.FIELD_PARAM,
                                                   MetiersTable.FIELD_VALUE
                                                   ))

        with open(self.path) as file:
            rows = tuple(csv.reader(file, delimiter=" "))

        print("Loading: {}".format(os.path.abspath(self.path)))

        for row in rows[1:]:
            if len(row) < 2:
                continue
            db.execute(row[0], "RevCompleteness", row[1])
        db.commit()
