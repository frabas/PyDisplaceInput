from displace.importer import PopulationParametersWithSizeGroupImporter

class SelectedSzgroups(PopulationParametersWithSizeGroupImporter):
    def __init__(self):
        super(SelectedSzgroups, self).__init__(
            "popsspe_{name}/the_selected_szgroups.dat",
            "selected_szgroups"
        )
