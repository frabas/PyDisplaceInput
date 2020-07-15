import os

from displace.importer import Importer


class CalendarImporter():
    def __init__(self, calendarType, name, yearstart, yearend):
        #super(Importer, self).__init__("simusspe_{{name}}/tstep_{}_{}_{}.dat".format(calendarType, yearstart, yearend))
        self.path = "simusspe_{}/tstep_{}_{}_{}.dat".format(name,calendarType, yearstart, yearend)
        self.__paramName = "{}_{}_{}".format(calendarType, yearstart, yearend)

    def import_file(self, db):
        print("loading {}".format(os.path.abspath(self.path)))

        with open(self.path) as file:
            lines = file.readlines()

        value = ";".join([s.strip() for s in lines])
        db.insert_config_entry(self.__paramName, value);


class Calendar():
    def __init__(self, name):
        self.__name = name
        pass

    def import_files(self, db, yearstart, yearend):
        daysImporter = CalendarImporter("days", self.__name, yearstart, yearend)
        daysImporter.import_file(db)
        monthsImporter = CalendarImporter("months", self.__name, yearstart, yearend)
        monthsImporter.import_file(db)
        quartersImporter = CalendarImporter("quarters", self.__name, yearstart, yearend)
        quartersImporter.import_file(db)
        semestersImporter = CalendarImporter("semesters", self.__name, yearstart, yearend)
        semestersImporter.import_file(db)
        yearsImporter = CalendarImporter("years", self.__name, yearstart, yearend)
        yearsImporter.import_file(db)
