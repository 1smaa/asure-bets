from packages.decorators import catch
import functools


def query_override(f):
    '''
    Specifies the query based on the type.
    '''
    @functools.wraps(f)
    def wrapper(*args, **kwargs):
        print(args)
        t = args[0]
        if t == "SELECT":
            return SelectQuery()
        elif t == "INSERT":
            return InsertQuery()
        elif t == "DELETE":
            return DeleteQuery()
        elif t == "UPDATE":
            return UpdateQuery()
        else:
            raise Exception("Type not recognised")
    return wrapper


@query_override
def query(type: str) -> None:
    pass


class SelectQuery(object):
    def __init__(self) -> None:
        self.__base = "SELECT {attr} FROM {table} WHERE {conditions}"
        self.__query = ""

    def set(self, attr: list, table: str, conditions: dict) -> None:
        '''
        Resets the query and adds data.
        '''
        self.__query = self.__base.format(attr=','.join(attr),
                                          table=table,
                                          conditions=' AND '.join(map(lambda x: "{c}={r}".format(
                                               c=x, r=conditions[x] if not isinstance(conditions[x], str) and conditions[x] is not None else "'{y}'".format(y=conditions[x])), conditions.keys())) if conditions else "")
        if not conditions:
            self.__query = self.__query[:-7]

    def get(self) -> str:
        return self.__query


class InsertQuery(object):
    def __init__(self) -> None:
        self.__base = "INSERT INTO {table}{fields} VALUES {values}"
        self.__query = ""

    def set(self, table: str, fields: dict) -> None:
        '''
        Resets the DML query and adds the fields.
        '''
        self.__query = self.__base.format(table=table,
                                          fields="({})".format(
                                              ','.join(fields.keys())),
                                          values="({})".format(','.join(map(lambda x: str(fields[x]) if not isinstance(fields[x], str) else "'{}'".format(fields[x]), fields.keys()))))

    def get(self) -> str:
        return self.__query


class DeleteQuery(object):
    def __init__(self) -> None:
        self.__base = "DELETE FROM {table} WHERE {conditions}"
        self.__query = ""

    def set(self, table: str, conditions: dict) -> None:
        '''
        Resets the DML query and adds the conditions.
        '''
        self.__query = self.__base.format(table=table,
                                          conditions=' AND '.join(map(lambda x: "{c}={r}".format(
                                              c=x, r=conditions[x] if not isinstance(conditions[x], str) else "'{y}'".format(y=conditions[x])), conditions.keys())))

    def get(self) -> str:
        return self.__query


class UpdateQuery(object):
    def __init__(self) -> None:
        self.__base = "UPDATE {table} SET {attr} WHERE {conditions}"
        self.__query = ""

    def __format(self, data: dict) -> str:
        return ','.join(map(lambda x: "{c}={r}".format(
            c=x, r="'{y}'".format(y=data[x]) if isinstance(data[x], str) or data[x] is None else data[x]), data.keys()))

    def set(self, table: str, attr: dict, conditions: dict) -> None:
        '''
        Resets the DML query and adds set and conditions.
        '''
        self.__query = self.__base.format(table=table,
                                          attr=self.__format(attr),
                                          conditions=self.__format(conditions))

    def get(self) -> str:
        return self.__query
