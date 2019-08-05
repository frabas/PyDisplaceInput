from displace.importer import HashFileImporter


class Config(HashFileImporter):
    params = ("nbpops", "nbbenthospops", "implicit_stocks", "calib_landings_stock",
              "calib_w_at_szgroup_stock", "calib_cpue_stock", "Interesting_harbours",
              "implicit_pops_level2", "grouped_tacs", "nbcp_coupling_pops")

    def __init__(self):
        super(Config, self).__init__("simusspe_{name}/config.dat", self.__load)

        self.__nbpops = None
        self.__nbbenthos = None

    @property
    def nbpops(self):
        return self.__nbpops

    def __load(self, db, lines):
        self.__nbpops, self.__nbbenthos = map(int, lines[:2])

        for param, line in zip(self.params, lines):
            db.insert_config_entry(param, line)
