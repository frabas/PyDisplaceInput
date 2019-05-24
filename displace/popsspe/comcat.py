from displace.importer import PopulationParametersWithSizeGroupImporter


class Comcat(PopulationParametersWithSizeGroupImporter):
    def __init__(self):
        super(Comcat, self).__init__(
            "popsspe_{name}/comcat_per_szgroup_done_by_hand.dat",
            "comcat"
        )
