import os
from abc import ABC, abstractmethod

from displace.utils import nwise


class Importer(ABC):
    """An abstract class to import files into db"""

    def __init__(self, path):
        """
        The main constructor, no parameters.
        """

        self.__pathformat = path
        self.__path = path

    def setpath(self, name, **kwargs):
        self.__path = self.__pathformat.format(name=name, **kwargs)

    @property
    def path(self):
        return self.__path

    @abstractmethod
    def import_file(self, db):
        """
        Import the file into the passed db object
        """

        pass


class NSplitsFileImporter(Importer):
    def __init__(self, path, splits, op):
        super(NSplitsFileImporter, self).__init__(path)

        self.__splits = splits
        self.__op = op

    def import_file(self, db):
        print("loading {}".format(os.path.abspath(self.path)))

        with open(self.path) as file:
            # strip whitespace from all lines and remove empty ones
            lines = tuple(filter(None, map(str.strip, file.readlines())))

            div, mod = divmod(len(lines), self.__splits)

            if mod:
                ValueError("File {} has illegal format".format(self.path))

            entries = nwise(lines, self.__splits, div)

            self.__op(db, entries)


class HashFileImporter(Importer):
    def __init__(self, path, op):
        super(HashFileImporter, self).__init__(path)

        self.__op = op

    def import_file(self, db):
        print("loading {}".format(os.path.abspath(self.path)))

        with open(self.path) as file:
            self.__op(db, tuple(map(str.strip, file))[1::2])
