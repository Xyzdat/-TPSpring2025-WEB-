from database.db_conect import DBConnection
from pymysql.err import OperationalError

def select(dbconfig: dict, _sql: str):
    with DBConnection(dbconfig) as cursor:
        if cursor is None:
            return None
        else:
            cursor.execute(_sql)
            result = cursor.fetchall()
            schema = [column[0] for column in cursor.description]
            output = []
            for row in result:
                output.append(row)
            return output
        
def select_string(db_config: dict, _sql: str):
    result = dict()
    schema = list()
    print(_sql)

    with DBConnection(db_config) as cursor:

        if cursor is None:
            raise ValueError("Cursor not created")
        else:
            try:
                cursor.execute(_sql)
                result = cursor.fetchall()
            except OperationalError as error:
                print("error: ", error)
                return result
            else:
                print("Cursor no errors")

            schema = [item[0] for item in cursor.description]

    return result, schema

def select_proc(dbconfig: dict, _sql: str):
    print(_sql)
    with DBConnection(dbconfig) as cursor:
        if cursor is None:
            return None
        else:
            cursor.execute(_sql)
            # Check if the procedure returned any results
            if cursor.description is not None:
                result = cursor.fetchall()
                schema = [column[0] for column in cursor.description]
                output = [dict(zip(schema, row)) for row in result]
                return output
            else:
                # Procedure executed, but there are no results
                return []


def select_insert(dbconfig: dict, _sql: str):
     with DBConnection(dbconfig) as cursor:
        if cursor is None:
            return None
        else:
            return cursor.execute(_sql)
        
def select_insert_ord(dbconfig: dict, _sql: str):
     with DBConnection(dbconfig) as cursor:
        if cursor is None:
            return None
        else:
            cursor.execute(_sql)
            res = cursor.lastrowid
            return res

def select_id(dbconfig: dict, _sql: str):
    with DBConnection(dbconfig) as cursor:
        if cursor is None:
            return None
        else:
            cursor.execute(_sql)
            result = cursor.fetchall()
            res = cursor.lastrowid
            schema = [column[0] for column in cursor.description]
            output = []
            for row in result:
                output.append(row[0])
            return output