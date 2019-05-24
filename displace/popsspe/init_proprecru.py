from displace.importer import PopulationParametersWithSizeGroupImporter


class InitProprecru(PopulationParametersWithSizeGroupImporter):
    def __init__(self):
        super(InitProprecru, self).__init__(
            "popsspe_{name}/init_proprecru_per_szgroup_biolsce{biosce}.dat",
            "proprecru"
        )
