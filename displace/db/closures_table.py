class ClosuresTable:
    TABLE_NAME = "ClosuresSpe"
    FIELD_CLOSURESCE = "ClosureSce"
    FIELD_ID = "ClosureId"
    FIELD_NODE = "NodeId"
    FIELD_TYPE = "Type"
    FIELD_PERIOD = "Period"
    FIELD_OPT = "Opt"
    FIELD_VALUE = "Closures"

    def __init__(self):
        pass

    def prepare_insert(*fields):
        fields_list = ", ".join(map(str, fields))
        qmark_list = ", ".join(map(str, "?" * len(fields)))
        sql = "INSERT INTO {}({}) VALUES({}) ".format(ClosuresTable.TABLE_NAME, fields_list, qmark_list)
        return sql
