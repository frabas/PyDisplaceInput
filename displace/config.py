from displace.importer import Importer


class Config(Importer):
    lines = ["nbpops", "nbbenthospops", "implicit_stocks", "calib_landings_stock",
             "calib_w_at_szgroup_stock", "calib_cpue_stock", "Interesting_harbours"]

    def __init__(self):
        super().__init__("simusspe_{}/config.dat")

        self.__nbpops = None
        self.__nbbenthos = None

    @property
    def nbpops(self):
        return self.__nbpops

    def import_file(self, db):

        fld = 0
        params = []
        with open(self.path) as file:
            for line in file:
                line = line.strip()
                if line.startswith("#"):
                    continue
                db.insert_config_entry(self.lines[fld], line)
                params.append(line)
                fld = fld + 1
                if fld >= len(self.lines):
                    break

        self.__nbpops = int(params[0])
        self.__nbbenthos = int(params[1])
