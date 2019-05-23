from displace.importer import PopulationParametersImporter


class SsbR(PopulationParametersImporter):
    FILENAME_FORMAT = "popsspe_{name}/{{popid}}spe_SSB_R_parameters_biolsce{{biosce}}.dat"
    PARAMETERS = "SSB_R_1", "SSB_R_2", "SSB_R_3"
