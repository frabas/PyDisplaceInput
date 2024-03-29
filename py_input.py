#!/usr/bin/env python3
"""
A tool to read, translate and fill the displace input data (txt files) into a SQLite file
"""

from argparse import ArgumentParser

from displace.config import Config
from displace.calendar import Calendar
from displace.graphsspe.closures import *
from displace.graphsspe.coordnodes import *
from displace.graphsspe.graphedges import GraphEdges
from displace.popsspe.avai_beta_semester import AvaiBetaSemester
from displace.popsspe.comcat import Comcat
from displace.popsspe.hyperstability import Hyperstability
from displace.popsspe.init_fecondity import InitFecondity
from displace.popsspe.init_m import InitM
from displace.popsspe.selected_szgroups import SelectedSzgroups
from displace.popsspe.init_maturity import InitMaturity
from displace.popsspe.init_pops import InitPops
from displace.popsspe.init_prop_migrants_pops import InitPropMigrantsPops
from displace.popsspe.init_proprecru import InitProprecru
from displace.popsspe.init_weight import InitWeight
from displace.popsspe.percent_age import PercentAge
from displace.popsspe.percent_szgroup import PercentSzGroup
from displace.popsspe.spe_base import SpeBase
from displace.popsspe.spe_initial_tac import SpeInitialTac
from displace.popsspe.spe_relative_stability import SpeRelativeStability
from displace.popsspe.spe_size_transition_matrix import SpeSizeTransitionMatrix
from displace.popsspe.spe_ssb_r import SsbR
from displace.popsspe.static_avai import StaticAvaiFull
from displace.popsspe.oth_land import OthLand
from displace.benthosspe.hab_delta_pop import SpeDeltaHab
from displace.scenario import Scenario
from displace.scenarioconfig import ScenarioConfig
from displace.vesselsspe.vesselfeatures import *
from displace.vesselsspe.vesselparameters import VesselPrices
from displace.vesselsspe.vesselscharacters import *
from displace.fishfarmsspe.fishfarmfeatures import *
from displace.shipsspe.shipfeatures import *
from displace.shipsspe.shipparameters import ShipLanesLat
from displace.shipsspe.shipparameters import ShipLanesLon
from displace.firmsspe.firmfeatures import *
from displace.harboursspe.harbourfeatures import *
from displace.harboursspe.harbourfishprice import HarbourFishPrice
from displace.harboursspe.harbourfuelprice import HarbourFuelPrice
from displace.benthosspe.carrying_cap_funcgrp import BenthosCarryingCap
from displace.benthosspe.mean_weight_funcgrp import BenthosMeanWeight
from displace.benthosspe.recovery_rate_funcgrp import BenthosRecoveryRate
from displace.benthosspe.prop_funcgrp import BenthosPropPerLandscape
from displace.metiersspe.metierfeatures import *
from displace.metiersspe.loss_with_one_trawl_path import MetierDepletionOnHab
from displace.metiersspe.selectivity_ogive_per_pop import *


class PyInput:
    tables = (
        ScenarioConfig(),
        CoordNodes(), NodesCodeArea(), NodesMarineLandscape(), NodesWind(),
        NodesSalinity(), NodesSST(), NodesNitrogen(), NodesPhosphorus(),
        NodesOxygen(), NodesCarbon(), NodesBathymetry(), NodesShipping(),
        NodesSilt(), NodesBenthosBio(), NodesBenthosNum(),
        GraphEdges(),
        SpeBase(), SpeInitialTac(), SsbR(), PercentAge(), Hyperstability(),
        PercentSzGroup(), InitWeight(), InitM(), SelectedSzgroups(), InitMaturity(), InitFecondity(), InitPops(), Comcat(),
        InitProprecru(), InitPropMigrantsPops(), SpeSizeTransitionMatrix(), SpeRelativeStability(),
        AvaiBetaSemester(), StaticAvaiFull(), OthLand(), SpeDeltaHab(),
        VesselEconomicFeatures(), VesselInitialCredit(),
        VesselFeatures(), VesselFishGrounds(), VesselFishHarbours(), VesselsPercentTacs(), VesselsBetas(),
        VesselPossibleMetiers(),
        VesselShapeCpueOnNodes(), VesselScaleCpueOnNodes(), VesselCpueOnNodes(),
        VesselPrices(),
        ClosuresMetier(), ClosuresVSize(),
        FishfarmFeatures(),
        ShipFeatures(), ShipLanesLat(), ShipLanesLon(),
        FirmFeatures(),
        HarbourFeatures(), HarbourFishPrice(), HarbourFuelPrice(),
        BenthosCarryingCap(), BenthosMeanWeight(), BenthosRecoveryRate(), BenthosPropPerLandscape(),
        MetierFeatures(), MetierDepletionOnHab(), MetierSelOgive(), MetierSelOgiveOth(),
        MetierTargetStock(), MetierSpeedAtFishing(), MetierType(), MetierGearWidthModel(), MetierGearWidthA(),
        MetierGearWidthB(),
        MetierSuitableBottomType(), MetierRevenueCompleteness(),
        MetierBeta(), MetierDiscardRatio(), MetierStockIsAvoided(), MetierStockMLS(),
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
        self.__this_path = os.path.dirname(__file__)

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
            print("Running from: {}".format(os.getcwd()))
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
        self.__dbobj.create_schema(self.__this_path)

        os.chdir(self.__inputdir)

        config = Config()
        config.setpath(self.__name)
        config.import_file(self.__dbobj)

        calendar = Calendar(self.__name)
        calendar.import_files(self.__dbobj, 2009, 2015)

        scenario = Scenario()
        scenario.setpath(self.__name, scenario=self.__scenario)
        scenario.import_file(self.__dbobj)

        self.__dbobj.biosce = scenario.biosce
        self.__dbobj.graphsce = scenario.graphsce
        self.__dbobj.fleetsce = scenario.fleetsce

        self.__dbobj.create_scenario(self.__scenario, self.__notes)
        self.__dbobj.create_populations(config.nbpops)

        for table in self.tables:
            table.setpath(self.__name, graphsce=scenario.graphsce, biosce=scenario.biosce, scenario=self.__scenario)
            table.import_file(self.__dbobj)

    def input(self):
        return self.__inputdir


if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("--name", "-n", required=True, help="Scenario name")
    parser.add_argument("--notes", help="Scenario notes")
    parser.add_argument("--directory", "-d",
                        help="Location of the input files, default is the current working directory")
    parser.add_argument("--verbose", "-v", action="store_true", help="Make a verbose output on the console")
    parser.add_argument("--overwrite", "-w", action="store_true", help="Overwrite the output file if exists")
    parser.add_argument("--outfile", "-o",
                        help="The name of the db file that will receive the result. If existing, it will be overwritten")
    parser.add_argument("--encoding", "-X",
                        help="The text encoding to use, the default is the preferred encoding for this system, usually utf-8")
    parser.add_argument("sce", help="Scenario name, it will be also the name of the db file if no --outfile is specified (ex: baseline)")
    args = parser.parse_args()

    program = PyInput()
    if args.verbose:
        program.set_verbose(True)

    if args.encoding:
        Importer.Encoding = args.encoding

    if args.directory is None:
        program.set_input(os.path.curdir)
    else:
        program.set_input(args.directory)

    if args.outfile is None:
        outfile = args.sce + ".db"
    else:
        outfile = args.outfile

    outputpath = os.path.split(outfile)
    if not outputpath[0]:
        destpath=program.input()
    else:
        destpath=outputpath[0]

    program.set_scenario(args.name, args.notes, args.sce)
    program.set_output(os.path.join(destpath, outputpath[1]), args.overwrite)

    program.run()
