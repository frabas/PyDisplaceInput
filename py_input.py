#!/usr/bin/env python3
"""
A tool to read, translate and fill the displace input data (txt files) into a SQLite file
"""

import os
from argparse import ArgumentParser

from displace.config import Config
from displace.database import Database
from displace.graphsspe.coordnodes import CoordNodes
from displace.graphsspe.graphedges import GraphEdges
from displace.popsspe.hyperstability import Hyperstability
from displace.popsspe.init_m import InitM
from displace.popsspe.init_weight import InitWeight
from displace.popsspe.percent_age import PercentAge
from displace.popsspe.percent_szgroup import PercentSzGroup
from displace.popsspe.spe_base import SpeBase
from displace.popsspe.spe_initial_tac import SpeInitialTac
from displace.popsspe.spe_ssb_r import SsbR
from displace.scenario import Scenario


class PyInput:
    tables = (
        Hyperstability(), CoordNodes(), GraphEdges(), SpeBase(), SpeInitialTac(), SsbR(), PercentAge(),
        PercentSzGroup(), InitWeight(), InitM()
    )

    def __init__(self):
        self.__verbose = False
        self.__inputdir = None
        self.__overwrite = False
        self.__db = None
        self.__name = None
        self.__scenario = None
        self.__notes = None
        self.__dbobj = None

    def set_verbose(self, verbose):
        self.__verbose = verbose

    def set_input(self, indir):
        self.__inputdir = indir

    def set_output(self, db, overwrite=False):
        self.__overwrite = overwrite
        self.__db = db

    def set_scenario(self, name, notes, sce):
        self.__name = name
        self.__notes = notes
        self.__scenario = sce

    def run(self):
        if self.__verbose:
            print("Parsing {} directory, output db to: {}".format(self.__inputdir, self.__db))
        if os.path.exists(self.__db):
            # Todo: since many scenario can be added to the same db, overwrite should not work this way. Ok for now.
            if not self.__overwrite:
                print("File {} exists, I'll not overwrite it.".format(self.__db))
                exit(1)
            if self.__verbose:
                print("Removing output file {}".format(self.__db))
            os.remove(self.__db)
        self.__dbobj = Database(file=self.__db)
        self.__dbobj.create_schema()

        os.chdir(self.__inputdir)

        config = Config()
        config.setpath(self.__name)
        config.import_file(self.__dbobj)

        scenario = Scenario()
        scenario.setpath(self.__name, scenario=self.__scenario)
        scenario.import_file(self.__dbobj)

        self.__dbobj.biosce = scenario.biosce
        self.__dbobj.graphsce = scenario.graphsce
        self.__dbobj.fleetsce = scenario.fleetsce

        self.__dbobj.create_scenario(self.__name, self.__notes)
        self.__dbobj.create_populations(config.nbpops)

        for table in self.tables:
            table.setpath(self.__name, biosce=scenario.biosce)
            table.import_file(self.__dbobj)


if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("--name", "-n", required=True, help="Scenario name")
    parser.add_argument("--notes", help="Scenario notes")
    parser.add_argument("--sce", "-s", required=True, help="Scenario file name (ex: baseline)")
    parser.add_argument("--directory", "-d",
                        help="Location of the input files, default is the current working directory")
    parser.add_argument("--verbose", "-v", action="store_true", help="Make a verbose output on the console")
    parser.add_argument("--overwrite", "-o", action="store_true", help="Overwrite the output file if exists")
    parser.add_argument("outfile",
                        help="The name of the db file that will receive the result. If existing, it will be overwritten")
    args = parser.parse_args()

    program = PyInput()
    if args.verbose:
        program.set_verbose(True)

    if args.directory is None:
        program.set_input(os.path.curdir)
    else:
        program.set_input(args.directory)

    program.set_scenario(args.name, args.notes, args.sce)
    program.set_output(args.outfile, args.overwrite)

    program.run()
