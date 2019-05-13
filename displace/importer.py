"""An abstract class to import files into db"""


class Importer:
    """
    The main constructor, no parameters.
    """

    def __init__(self, path):
        self.__pathformat = path
        self.__path = path

    def setpath(self, name):
        self.__path = self.__pathformat.format(name)

    @property
    def path(self):
        return self.__path

    """
    Import the file into the passed db object
    """

    def import_file(self, db):
        pass
