from displace.importer import SingleRowPopulationParametersImporter


class SsbR(SingleRowPopulationParametersImporter):
    def __init__(self):
        super(SsbR, self).__init__(
            "popsspe_{name}/{{popid}}spe_SSB_R_parameters_biolsce{biosce}.dat",
            ("SSB_R_1", "SSB_R_2", "SSB_R_3")
        )
