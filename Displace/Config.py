from Displace.Importer import Importer


class Config(Importer):
    lines = ["nbpops", "nbbenthospops", "implicit_stocks", "calib_landings_stock",
             "calib_w_at_szgroup_stock", "calib_cpue_stock", "Interesting_harbours"]

    def __init__(self):
        super().__init__("simusspe_{}/config.dat")

    @property
    def nbpops(self):
        return self._nbpops

    def importFile(self, db):

        fld = 0
        params = []
        with open(self.path) as file:
            for line in file:
                line = line.strip()
                if line.startswith("#"):
                    continue
                db.insertConfigEntry(self.lines[fld], line)
                params.append(line)
                fld = fld + 1
                if fld >= len(self.lines):
                    break

        self._nbpops = int(params[0])
        self._nbbenthos = int(params[1])
