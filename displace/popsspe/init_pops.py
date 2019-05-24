from displace.importer import PopulationParametersWithSizeGroupImporter


class InitPops(PopulationParametersWithSizeGroupImporter):
    def __init__(self):
        super(InitPops, self).__init__(
            "popsspe_{name}/init_pops_per_szgroup_biolsce{biosce}.dat",
            "init_popN"
        )
