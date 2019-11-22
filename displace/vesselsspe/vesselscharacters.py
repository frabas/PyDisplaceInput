import csv
import glob
import os
import re
from abc import abstractmethod

from displace.db.vessels_table import VesselsTable
from displace.importer import Importer


class VesselCharacterImporter(Importer):
    @abstractmethod
    def checkMatch(self, path):
        """
        Checks if the path must be processed by the importer. Must return a TRUE and dic with the matching values
        in particular, "name" and "period"
        :param path: path of file being processed
        :return: a tuple of bool (TRUE or FALSE) and a dict with the extracted values
        """
        pass

    def do_import_file(self, db, keyword):
        files = glob.glob(self.path)

        db.prepare_sql(VesselsTable.prepare_insert(VesselsTable.FIELD_NAME,
                                                   VesselsTable.FIELD_PARAM,
                                                   VesselsTable.FIELD_OPT1,
                                                   VesselsTable.FIELD_OPT2,
                                                   VesselsTable.FIELD_PERIOD,
                                                   VesselsTable.FIELD_VALUE
                                                   ))
        for file in files:
            match, vars = self.checkMatch(file)
            if not match:
                continue

            print("loading {}".format(os.path.abspath(file)))
            with open(file) as f:
                rows = tuple(csv.reader(f, delimiter=" "))

            for row in rows[1:]:
                if len(row) < 2:
                    continue
                opt1 = row[0]
                value = row[1]
                db.execute(vars['name'], keyword, opt1, None, vars['period'], value)

        db.commit()


'''
 class VesselPossibleMetier(VesselCharacterImporter):
    def __init__(self):
        super().__init__("vesselsspe_{name}/*_possible_metiers_quarter*.dat")
        self.__re = re.compile("([A-Za-z0-9]+)_possible_metiers_quarter([0-9]).dat")

    def checkMatch(self, path):
        m = self.__re.match(os.path.basename(path))
        if m is None:
            return False, None

        vessel_name = m.group(1)
        quarter = m.group(2)

        return True, {'period': quarter, 'name': vessel_name}

    def import_file(self, db):
        return self.do_import_file(db, "PossibleMetier")


class VesselFreqPossibleMetier(VesselCharacterImporter):
    def __init__(self):
        super().__init__("vesselsspe_{name}/*_freq_possible_metiers_quarter*.dat")
        self.__re = re.compile("([A-Za-z0-9]+)_freq_possible_metiers_quarter([0-9]).dat")

    def checkMatch(self, path):
        m = self.__re.match(os.path.basename(path))
        if m is None:
            return False, None

        vessel_name = m.group(1)
        quarter = m.group(2)

        return True, {'period': quarter, 'name': vessel_name}

    def import_file(self, db):
        return self.do_import_file(db, "FreqPossibleMetier")
'''


class VesselShapeCpueOnNodes(VesselCharacterImporter):
    def __init__(self):
        super().__init__("vesselsspe_{name}/*_gshape_cpue_per_stk_on_nodes_quarter*.dat")
        self.__re = re.compile("([A-Za-z0-9]+)_gshape_cpue_per_stk_on_nodes_quarter([0-9]).dat")

    def checkMatch(self, path):
        m = self.__re.match(os.path.basename(path))
        if m is None:
            return False, None

        vessel_name = m.group(1)
        quarter = m.group(2)

        return True, {'period': quarter, 'name': vessel_name}

    def import_file(self, db):
        return self.do_import_file(db, "GShapeLPUE")


class VesselScaleCpueOnNodes(VesselCharacterImporter):
    def __init__(self):
        super().__init__("vesselsspe_{name}/*_gscale_cpue_per_stk_on_nodes_quarter*.dat")
        self.__re = re.compile("([A-Za-z0-9]+)_gscale_cpue_per_stk_on_nodes_quarter([0-9]).dat")

    def checkMatch(self, path):
        m = self.__re.match(os.path.basename(path))
        if m is None:
            return False, None

        vessel_name = m.group(1)
        quarter = m.group(2)

        return True, {'period': quarter, 'name': vessel_name}

    def import_file(self, db):
        return self.do_import_file(db, "GScaleLPUE")


class VesselCpueOnNodes(VesselCharacterImporter):
    def __init__(self):
        super().__init__("vesselsspe_{name}/*_cpue_per_stk_on_nodes_quarter*.dat")
        self.__re = re.compile("([A-Za-z0-9]+)_cpue_per_stk_on_nodes_quarter([0-9]).dat")

    def checkMatch(self, path):
        m = self.__re.match(os.path.basename(path))
        if m is None:
            return False, None

        vessel_name = m.group(1)
        quarter = m.group(2)

        return True, {'period': quarter, 'name': vessel_name}

    def import_file(self, db):
        return self.do_import_file(db, "FixedLPUE")
