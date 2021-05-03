
class HarboursTable:
    TABLE_NAME = "HarboursParameters"
    FIELD_NAME = "harbour_name"
    FIELD_NODE = "node_id"
    FIELD_PARAM = "parameter"
    FIELD_OPT1 = "opt1"
    FIELD_OPT2 = "opt2"
    FIELD_PERIOD = "period"
    FIELD_VALUE = "value"

    def __init__(self):
        pass

    def prepare_insert(*fields):
        fields_list = ", ".join(map(str,fields))
        qmark_list = ", ".join(map(str,"?"*len(fields)))
        sql = "INSERT INTO {}({}) VALUES({}) ".format(HarboursTable.TABLE_NAME, fields_list, qmark_list)
        return sql
