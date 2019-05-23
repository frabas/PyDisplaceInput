from displace.importer import MatrixImporter

class PercentSzGroup(MatrixImporter):
    FILENAME_FORMAT = "popsspe_{name}/{{popid}}spe_percent_szgroup_per_age_biolsce{biosce}.dat"
    PARAMETER_NAME = "percent_szgroup_per_age"
