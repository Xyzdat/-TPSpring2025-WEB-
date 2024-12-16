import pymysql
from pymysql import OperationalError

db_config = {
    'port' : 3306,
    'host': '127.0.0.1',
    'password': "1234",
    'db' : 'flower_delivery',
    'user': 'root'
    # 'cursorclass': pymysql.cursors.DictCursor
}

class DBConnection:
    def __init__(self, db_config):
        self.db_config = db_config
        self.connection = None
        self.cursor = None

    def __enter__(self):
        try:
            self.connection = pymysql.connect(
                **self.db_config
                )
            self.cursor = self.connection.cursor()
            return self.cursor
        except (OperationalError, KeyError) as err:
            print(err.args)
            return None
             
    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.connection is not None and self.cursor is not None:
            if exc_type:
                print(exc_type)
                print(exc_val)
                self.connection.rollback()
            else:
                self.connection.commit()
            self.cursor.close()
            self.connection.close()
        return True #чтобы в консоль не падала ошибка красным
