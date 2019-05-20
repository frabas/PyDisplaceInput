from displace.importer import PopulationParametersImporter


class SpeInitialTac(PopulationParametersImporter):
    FILENAME_FORMAT = "{popid}spe_initial_tac.dat"
    PARAMETERS = "initial_tac"
