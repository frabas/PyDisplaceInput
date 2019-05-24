from displace.importer import SizeAgeMatrixImporter

class PercentSzGroup(SizeAgeMatrixImporter):
    def __init__(self):
        super(PercentSzGroup, self).__init__(
            "popsspe_{name}/{{popid}}spe_percent_szgroup_per_age_biolsce{biosce}.dat",
            "percent_szgroup_per_age"
        )
