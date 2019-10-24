import csv
import os
from abc import ABC, abstractmethod

from displace.utils import nwise


class Importer(ABC):
    """
    An abstract class to import files into db
    """

    def __init__(self, path):
        self.__pathformat = path
        self._path_params = {}
        self.__path = path

    def setpath(self, name, **kwargs):
        self._path_params = kwargs

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

        op(db, ((<a0>, <b0>, <c0>), (<a1>, <b1>, <c1>), (<a2>, <b2>, <c2>)))

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
    Importer for files with parameters separated by hash comments:

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


class SingleRowPopulationParametersImporter(Importer, ABC):
    """
    Importer for files with named population parameters separated by space on a single row or column

    Example:

        File:

        <param0> <param1> <param2> ...

        Result:

        Insertion in db of parameters with the provided names

    """

    def __init__(self, path, parameters):
        """
        :param parameters: Positional names for the parameters
        """

        super(SingleRowPopulationParametersImporter, self).__init__(path)

        self.__parameters = parameters

    def import_file(self, db):
        for popid in db.find_all_populations_ids():
            path = self.path.format(popid=popid)

            print("loading {}".format(os.path.abspath(path)))

            with open(path) as f:
                # noinspection PyShadowingBuiltins
                all = first, *others = tuple(csv.reader(f))


            if others:  # If values are in one column instead of one line
                values = (r for r, in all)  # Keep just the first line (raise error if more)

            else:
                values = first


            for param, value in zip(self.__parameters, values):
                db.insert_population_parameter(popid, param, value)


class SizeAgeMatrixImporter(Importer, ABC):
    """
    Importer for files with matrix like structure, indexed by size group and age group
    """

    def __init__(self, path, parameter_name):
        super(SizeAgeMatrixImporter, self).__init__(path)

        self.__parameter_name = parameter_name

    def import_file(self, db):
        db.prepare_insert_population_parameter_with_szgroup_and_age()

        for popid in db.find_all_populations_ids():
            path = self.path.format(popid=popid)

            print("loading {}".format(os.path.abspath(path)))

            with open(path) as f:
                for szgroup, vals in enumerate(csv.reader(f, delimiter=" ")):
                    for age, value in enumerate(vals):
                        db.insert_population_parameter_with_szgroup_and_age(
                            popid, self.__parameter_name, value, szgroup, age
                        )

        db.commit_insert_population_parameter_with_szgroup_and_age()


class PopulationParametersWithSizeGroupImporter(Importer, ABC):
    """
    Importer for files with a header, pop_id on first column and parameter value on second column
    """

    def __init__(self, path, parameter_name):
        super(PopulationParametersWithSizeGroupImporter, self).__init__(path)

        self.__parameter_name = parameter_name

    def import_file(self, db):
        print("loading {}".format(os.path.abspath(self.path)))

        with open(self.path) as file:
            rows = tuple(csv.reader(file, delimiter=" "))

        prev_pop_id = None
        size_group = 0

        db.prepare_insert_population_parameter_with_szgroup_and_age()
        for popid, param in rows[1:]:
            if popid != prev_pop_id:
                prev_pop_id = popid
                size_group = 0

            else:
                size_group += 1

            db.insert_population_parameter_with_szgroup_and_age(popid, self.__parameter_name, param, size_group)

        db.commit_insert_population_parameter_with_szgroup_and_age()
