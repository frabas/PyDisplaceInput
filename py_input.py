#!/usr/bin/env python
"""
A tool to read, translate and fill the displace input data (txt files) into a SQLite file
"""

import os
from argparse import ArgumentParser

from displace.config import Config
from displace.database import Database
from displace.popsspe.hyperstability import Hyperstability


class PyInput:
    listOfTables = [Hyperstability()]

    def __init__(self):
        self._verbose = False

    def setVerbose(self, verbose):
        self._verbose = verbose

    def setInput(self, indir):
        self._inputdir = indir

    def setOutput(self, db, overwrite=False):
        self._overwrite = overwrite
        self._db = db

    def setScenario(self, scenario, scenario_name=None, scenarion_notes=None):
        self._biosce = scenario
        self._biosce_name = scenario_name
        self._biosce_notes = scenarion_notes

    def run(self):
        if self._verbose:
            print("Parsing {} directory, output db to: {}".format(self._inputdir, self._db))
        if os.path.exists(self._db):
            # Todo: since many scenario can be added to the same db, overwrite should not work this way. Ok for now.
            if not self._overwrite:
                print("File {} exists, I'll not overwrite it.".format(self._db))
                exit(1)
            if self._verbose:
                print("Removing output file {}".format(self._db))
            os.remove(self._db)
        self._dbobj = Database(file=self._db, biosce=self._biosce)
        self._dbobj.create_schema()
        self._dbobj.create_scenario(self._biosce_name, self._biosce_notes)

        os.chdir(self._inputdir)

        config = Config()
        config.setpath(self._biosce_name)
        config.import_file(self._dbobj)
        self._dbobj.create_populations(config.nbpops)

        for table in self.listOfTables:
            table.setpath(self._biosce_name)
            table.import_file(self._dbobj)


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
        program.setVerbose(True)

    if args.directory is None:
        program.setInput(os.path.curdir)
    else:
        program.setInput(args.directory)

    program.setScenario(args.biosce, args.biosce_name, args.biosce_notes)
    program.setOutput(args.outfile, args.overwrite)

    program.run()
