from displace.importer import PopulationParametersWithSizeGroupImporter


class InitMaturity(PopulationParametersWithSizeGroupImporter):
    def __init__(self):
        super(InitMaturity, self).__init__(
            "popsspe_{name}/init_maturity_per_szgroup_biolsce{biosce}.dat",
            "init_mat"
        )
