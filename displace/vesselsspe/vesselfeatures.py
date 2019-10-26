import csv
import os

from displace.importer import Importer
from ..db.vessels_table import VesselsTable


class VesselFeaturesImporter(Importer):
    def do_import(self, db, path=None, quarter=None):
        if path is None:
            path = self.path
        print("loading {}".format(os.path.abspath(path)))

        with open(path) as file:
            rows = tuple(csv.reader(file, delimiter="|"))

        db.prepare_sql(VesselsTable.prepare_insert(VesselsTable.FIELD_NAME,
                                                   VesselsTable.FIELD_PARAM,
                                                   VesselsTable.FIELD_OPT1,
                                                   VesselsTable.FIELD_VALUE,
                                                   VesselsTable.FIELD_PERIOD
                                                   ))

        for row in rows:
            vessel_name = row[0]
            self.insert_vessel(db, vessel_name)
            for i, feature in enumerate(row[1:]):
                db.execute(vessel_name, self.feature_name, i + 1, feature, quarter)

        db.commit()

    def insert_vessel(self, db, vessel_name):
        pass


class VesselFeatures(VesselFeaturesImporter):
    def __init__(self):
        self.feature_name = "feature"
        super().__init__("vesselsspe_{name}/vesselsspe_features_quarter{{quarter}}.dat")

    def import_file(self, db):
        for quarter in 1, 2, 3, 4:
            path = self.path.format(quarter=quarter)
            self.do_import(db, quarter=quarter, path=path)


class VesselEconomicFeatures(VesselFeaturesImporter):
    def __init__(self):
        self.feature_name = "economic_feature"
        super().__init__("vesselsspe_{name}/vesselsspe_economic_features.dat")

    def insert_vessel(self, db, vessel_name):
        db.insert_vessel(vessel_name)

    def import_file(self, db):
        self.do_import(db)


class VesselFishGrounds(Importer):
    def __init__(self):
        super().__init__("vesselsspe_{name}")

    def import_file(self, db):

        db.prepare_sql(VesselsTable.prepare_insert(VesselsTable.FIELD_NAME,
                                                   VesselsTable.FIELD_PARAM,
                                                   VesselsTable.FIELD_OPT1,
                                                   VesselsTable.FIELD_VALUE,
                                                   VesselsTable.FIELD_PERIOD
                                                   ))

        for quarter in 1, 2, 3, 4:
            fground_path = "{}/vesselsspe_fgrounds_quarter{}.dat".format(self.path, quarter)
            fg_freq_path = "{}/vesselsspe_freq_fgrounds_quarter{}.dat".format(self.path, quarter)

            print("Loading: {}".format(os.path.abspath(fground_path)))
            with open(fground_path) as file:
                fg_rows = tuple(csv.reader(file, delimiter=" "))

            print("Loading: {}".format(os.path.abspath(fg_freq_path)))
            with open(fg_freq_path) as file:
                fgf_rows = tuple(csv.reader(file, delimiter=" "))

            for row in zip(fg_rows[1:], fgf_rows[1:]):
                vessel_name = row[0][0]
                fgv = row[0][1]
                ffv = row[1][1]
                db.execute(vessel_name, "fgroundFreq", fgv, ffv, quarter)

        db.commit()


class VesselInitialCredit(VesselFeaturesImporter):
    def __init__(self):
        super().__init__("vesselsspe_{name}/initial_share_fishing_credits_per_vid.dat")

    def import_file(self, db):
        db.prepare_sql(VesselsTable.prepare_insert(VesselsTable.FIELD_NAME,
                                                   VesselsTable.FIELD_PARAM,
                                                   VesselsTable.FIELD_VALUE
                                                   ))

        with open(self.path) as file:
            rows = tuple(csv.reader(file, delimiter=" "))

        for row in rows[1:]:
            if len(row) < 2:
                continue
            db.execute(row[0], "CreditShare", row[1])
        db.commit()


class VesselsPercentTacsImporter(Importer):
    def import_file(self, db):
        db.prepare_sql(VesselsTable.prepare_insert(VesselsTable.FIELD_NAME,
                                                   VesselsTable.FIELD_PARAM,
                                                   VesselsTable.FIELD_OPT1,
                                                   VesselsTable.FIELD_VALUE,
                                                   VesselsTable.FIELD_PERIOD
                                                   ))

        for semester in 1, 2:
            path = self.path.format(semester=semester)

            print("Loading: {}".format(os.path.abspath(path)))
            with open(path) as file:
                rows = tuple(csv.reader(file, delimiter=" "))

            lastname = ""
            curpop = 0
            for row in rows[1:]:
                if len(row) < 2:
                    continue

                vessel_name = row[0]
                if lastname != vessel_name:
                    curpop = 0

                db.execute(vessel_name, self.param, curpop, row[1], semester)
                curpop = curpop + 1
                lastname = vessel_name

        db.commit()


class VesselsPercentTacs(VesselsPercentTacsImporter):
    def __init__(self):
        self.param = "percentTac"
        super().__init__("vesselsspe_{name}/vesselsspe_percent_tacs_per_pop_semester{{semester}}.dat")


class VesselsBetas(VesselsPercentTacsImporter):
    def __init__(self):
        self.param = "vesselBeta"
        super().__init__("vesselsspe_{name}/vesselsspe_betas_semester{{semester}}.dat")
