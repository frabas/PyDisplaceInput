from displace.importer import SizeAgeMatrixImporter

class PercentSzGroup(SizeAgeMatrixImporter):
    FILENAME_FORMAT = "popsspe_{name}/{{popid}}spe_percent_szgroup_per_age_biolsce{biosce}.dat"
    PARAMETER_NAME = "percent_szgroup_per_age"
