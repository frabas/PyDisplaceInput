from displace.importer import PopulationParametersImporter


class SpeBase(PopulationParametersImporter):
    FILENAME_FORMAT = "{popid}spe_fbar_amin_amax_ftarget_Fpercent_TACpercent.dat"
    PARAMETERS = "fbar_min", "fbar_max", "ftarget", "fpercent", "TACpercent", "Btrigger", "FMSY"
