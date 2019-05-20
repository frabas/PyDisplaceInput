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
    """
    Importer for files containing tuples of n elements (splits), grouped by position.

    Example:

        splits = 3

        File:

        <a0>
        <a1>
        <a2>
        <b0>
        <b1>
        <b2>
        <c0>
        <c1>
        <c2>

        Output:

        (<a0>, <b0>, <c0>), (<a1>, <b1>, <c1>), (<a2>, <b2>, <c2>)

    """

    def __init__(self, path, splits, op):
        """
        :param splits: Number of values per entry (aka: "splits" or "sections" of the file)
        :param op: A function to call with db and the parsed entries
        """
        super(NSplitsFileImporter, self).__init__(path)

        self.__splits = splits
        self.__op = op

    def import_file(self, db):
        print("loading {}".format(os.path.abspath(self.path)))

        with open(self.path) as file:
            # strip whitespace from all lines and remove empty ones
            lines = tuple(filter(None, map(str.strip, file)))

            div, mod = divmod(len(lines), self.__splits)

            if mod:
                ValueError("File {} has illegal format".format(self.path))

            entries = nwise(lines, self.__splits, div)

            self.__op(db, entries)


class HashFileImporter(Importer):
    """
    Importer for files with parameters commented via hash comments:

    Example:

        File:

        # <parameter name>
        <parameter0 value>
        # <parameter name>
        <parameter1 value>
        ...

        Result:

        op(db, (<parameter0>, <parameter1>, ...))

    """

    def __init__(self, path, op):
        """
        :param op: A function to call with db and the parsed parameters
        """

        super(HashFileImporter, self).__init__(path)

        self.__op = op

    def import_file(self, db):
        print("loading {}".format(os.path.abspath(self.path)))

        with open(self.path) as file:
            lines = map(str.strip, file)

            # Keep a line every other, skipping the first one
            parameters = tuple(lines)[1::2]

            self.__op(db, parameters)
