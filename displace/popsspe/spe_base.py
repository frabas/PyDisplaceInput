from displace.importer import SingleRowPopulationParametersImporter


class SpeBase(SingleRowPopulationParametersImporter):
    def __init__(self):
        super(SpeBase, self).__init__(
            "popsspe_{name}/{{popid}}spe_fbar_amin_amax_ftarget_Fpercent_TACpercent.dat",
            ("fbar_min", "fbar_max", "ftarget", "fpercent", "TACpercent", "Btrigger", "FMSY")
        )
