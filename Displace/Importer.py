"""An abstract class to import files into db"""


class Importer:
    """
    The main constructor, no parameters.
    """

    def __init__(self, pathformat):
        self._pathformat = pathformat

    def setpath(self, name):
        self._path = self._pathformat.format(name)

    @property
    def path(self):
        return self._path

    """
    Import the file into the passed db object
    """

    def importFile(self, db):
        pass
