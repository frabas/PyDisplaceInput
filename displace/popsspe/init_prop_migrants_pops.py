from displace.importer import PopulationParametersWithSizeGroupImporter


class InitPropMigrantsPops(PopulationParametersWithSizeGroupImporter):
    def __init__(self):
        super(InitPropMigrantsPops, self).__init__(
            "popsspe_{name}/init_prop_migrants_pops_per_szgroup_biolsce{biosce}.dat",
            "propmigrants"
        )
