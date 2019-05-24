from displace.importer import PopulationParametersWithSizeGroupImporter

class InitM(PopulationParametersWithSizeGroupImporter):
    def __init__(self):
        super(InitM, self).__init__(
            "popsspe_{name}/init_M_per_szgroup_biolsce{biosce}.dat",
            "init_M_per_szgroup"
        )
