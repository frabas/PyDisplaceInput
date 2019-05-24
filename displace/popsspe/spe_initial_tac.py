from displace.importer import SingleRowPopulationParametersImporter


class SpeInitialTac(SingleRowPopulationParametersImporter):
    def __init__(self):
        super(SpeInitialTac, self).__init__(
            "popsspe_{name}/{{popid}}spe_initial_tac.dat",
            "initial_tac"
        )
