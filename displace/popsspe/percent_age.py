from displace.importer import SizeAgeMatrixImporter

class PercentAge(SizeAgeMatrixImporter):
    def __init__(self):
        super(PercentAge, self).__init__(
            "popsspe_{name}/{{popid}}spe_percent_age_per_szgroup_biolsce{biosce}.dat",
            "percent_age_per_szgroup"
        )
