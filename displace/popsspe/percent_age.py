from displace.importer import MatrixImporter

class PercentAge(MatrixImporter):
    FILENAME_FORMAT = "popsspe_{name}/{{popid}}spe_percent_age_per_szgroup_biolsce{biosce}.dat"
    PARAMETER_NAME = "percent_age_per_szgroup"
