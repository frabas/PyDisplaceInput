#!/usr/bin/env python
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
from displace.popsspe.spebase import SpeBase


class PyInput:
    tables = Hyperstability(), CoordNodes(), GraphEdges(), SpeBase()

    def __init__(self):
        self.__verbose = False
        self.__inputdir = None
        self.__overwrite = False
        self.__db = None
        self.__biosce = None
        self.__biosce_name = None
        self.__biosce_notes = None
        self.__dbobj = None

    def set_verbose(self, verbose):
        self.__verbose = verbose

    def set_input(self, indir):
        self.__inputdir = indir

    def set_output(self, db, overwrite=False):
        self.__overwrite = overwrite
        self.__db = db

    def set_scenario(self, scenario, scenario_name=None, scenario_notes=None):
        self.__biosce = scenario
        self.__biosce_name = scenario_name
        self.__biosce_notes = scenario_notes

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
        self.__dbobj = Database(file=self.__db, biosce=self.__biosce)
        self.__dbobj.create_schema()
        self.__dbobj.create_scenario(self.__biosce_name, self.__biosce_notes)

        os.chdir(self.__inputdir)

        config = Config()
        config.setpath(biosce_name=self.__biosce_name)
        config.import_file(self.__dbobj)
        self.__dbobj.create_populations(config.nbpops)

        for table in self.tables:
            table.setpath(self.__biosce, self.__biosce_name)
            table.import_file(self.__dbobj)


if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("--biosce", "-b", type=int, required=True, help="Scenario number")
    parser.add_argument("--biosce_name", help="Scenario name", default="")
    parser.add_argument("--biosce_notes", help="Scenario notes", default="")
    parser.add_argument("--directory", "-d",
                        help="Location of the input files, default is the current working directory")
    parser.add_argument("outfile",
                        help="The name of the db file that will receive the result. If existing, it will be overwritten")
    parser.add_argument("--verbose", "-v", action="store_true", help="Make a verbose output on the console")
    parser.add_argument("--overwrite", "-o", action="store_true", help="Overwrite the output file if exists")
    args = parser.parse_args()

    program = PyInput()
    if args.verbose:
        program.set_verbose(True)

    if args.directory is None:
        program.set_input(os.path.curdir)
    else:
        program.set_input(args.directory)

    program.set_scenario(args.biosce, args.biosce_name, args.biosce_notes)
    program.set_output(args.outfile, args.overwrite)

    program.run()
