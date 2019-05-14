from abc import ABC, abstractmethod


class Importer(ABC):
    """An abstract class to import files into db"""

    def __init__(self, path):
        """
        The main constructor, no parameters.
        """

        self.__pathformat = path
        self.__path = path

    def setpath(self, name=None):
        self.__path = self.__pathformat.format(name)

    @property
    def path(self):
        return self.__path

    @abstractmethod
    def import_file(self, db):
        """
        Import the file into the passed db object
        """

        pass
