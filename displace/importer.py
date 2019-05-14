from abc import ABC, abstractmethod


class Importer(ABC):
    """An abstract class to import files into db"""

    def __init__(self, path):
        """
        The main constructor, no parameters.
        """

        self.__pathformat = path
        self.__path = path

    def setpath(self, biosce=None, biosce_name=None):
        assert biosce or biosce_name, "Must provide at least a parameter"

        self.__path = self.__pathformat.format(biosce=biosce, biosce_name=biosce_name)

    @property
    def path(self):
        return self.__path

    @abstractmethod
    def import_file(self, db):
        """
        Import the file into the passed db object
        """

        pass
