from displace.importer import PopulationParametersWithSizeGroupImporter

class InitWeight(PopulationParametersWithSizeGroupImporter):
    def __init__(self):
        super(InitWeight, self).__init__(
            "popsspe_{name}/init_weight_per_szgroup_biolsce{biosce}.dat",
            "init_weight_per_szgroup"
        )
