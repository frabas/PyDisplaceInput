from operator import itemgetter

from displace.importer import HashFileImporter


class Scenario(HashFileImporter):
    params = (
        2,  # biosce
        3,  # fleetsce
        6   # graphsce
    )

    def __init__(self):
        super(Scenario, self).__init__("simusspe_{name}/{scenario}.dat", self.__load)

        self.__biosce = None
        self.__fleetsce = None
        self.__graphsce = None

    @property
    def biosce(self):
        return self.__biosce

    @property
    def fleetsce(self):
        return self.__fleetsce

    @property
    def graphsce(self):
        return self.__graphsce

    def __load(self, _, lines):
        self.__biosce, self.__fleetsce, self.__graphsce = itemgetter(*self.params)(lines)
