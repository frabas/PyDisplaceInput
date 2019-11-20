
class FishfarmsTable:
    TABLE_NAME = "FishfarmsParameters"
    FIELD_NAME = "FishfarmName"
    FIELD_PARAM = "Parameter"
    FIELD_OPT1 = "Opt1"
    FIELD_OPT2 = "Opt2"
    FIELD_PERIOD = "Period"
    FIELD_VALUE = "Value"

    def __init__(self):
        pass

    def prepare_insert(*fields):
        fields_list = ", ".join(map(str,fields))
        qmark_list = ", ".join(map(str,"?"*len(fields)))
        sql = "INSERT INTO {}({}) VALUES({}) ".format(FishfarmsTable.TABLE_NAME, fields_list, qmark_list)
        return sql
