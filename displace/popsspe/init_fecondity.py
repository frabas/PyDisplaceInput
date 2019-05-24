from displace.importer import PopulationParametersWithSizeGroupImporter


class InitFecondity(PopulationParametersWithSizeGroupImporter):
    def __init__(self):
        super(InitFecondity, self).__init__(
            "popsspe_{name}/init_fecundity_per_szgroup_biolsce{biosce}.dat",
            "init_fec"
        )
