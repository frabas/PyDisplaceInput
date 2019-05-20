import csv
import os

from displace.importer import Importer


class SpeBase(Importer):
    FILENAME_FORMAT = "{}spe_fbar_amin_amax_ftarget_Fpercent_TACpercent.dat"
    PARAMETERS = 'fbar_min', 'fbar_max', 'ftarget', 'fpercent', 'TACpercent', 'Btrigger', 'FMSY'

    def __init__(self):
        super(SpeBase, self).__init__("popsspe_{name}")

    def import_file(self, db):
        for popid in db.find_all_populations_ids():
            path = os.path.join(self.path, SpeBase.FILENAME_FORMAT.format(popid))

            with open(path) as f:
                # Keep just the first line (raise error if more)
                values, = csv.reader(f, delimiter=" ")

            for param, value in zip(SpeBase.PARAMETERS, values):
                db.insert_population_parameter(popid, param, value)
