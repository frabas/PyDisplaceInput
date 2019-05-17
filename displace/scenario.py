from displace.importer import Importer


class Scenario(Importer):
    def __init__(self):
        super().__init__("")

        self.__biosce = 0
        self.__fleetsce = 0
        self.__graphsce = 1

    @property
    def biosce(self):
        return self.__biosce

    @property
    def fleetsce(self):
        return self.__fleetsce

    @property
    def graphsce(self):
        return self.__graphsce

    def import_file(self, db):
        pass
