#!/usr/bin/env python
"""
A tool to read, translate and fill the Displace input data (txt files) into a SQLite file
"""

import os
from argparse import ArgumentParser

from Displace.Database import Database


class PyInput:
    def __init__(self):
        self.verbose = False

    def setVerbose(self, verbose):
        self.verbose = verbose

    def run(self):
        if self.verbose:
            print("Parsing {} directory, output db to: {}".format(self.inputdir, self.db))
        if os.path.exists(self.db):
            if not self.overwrite:
                print("File {} exists, I'll not overwrite it.".format(self.db))
                exit(1)
            if self.verbose:
                print("Removing output file {}".format(self.db))
            os.remove(self.db)
        self.dbobj = Database(self.db)
        self.dbobj.createSchema()

    def setInput(self, indir):
        self.inputdir = indir

    def setOutput(self, db, overwrite=False):
        self.overwrite = overwrite
        self.db = db


if __name__ == "__main__":
    parser = ArgumentParser()
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

    program.setOutput(args.outfile, args.overwrite)

    program.run()
