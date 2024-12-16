from dataclasses import dataclass
from database.reqst import select_list

@dataclass
class Datastruture:
    result: tuple
    error_message: str
    status: bool


def model_route(dbconfig, user_data, sql_provider):
    error_message = ''
    if 'prod_category' not in user_data:
        result = ()
        return Datastruture(result, error_message= error_message, status = False)
    _sql = sql_provider.get('products.sql', prod_category = user_data['prod_category'])
    result, schema = select_list(dbconfig, _sql)
    return Datastruture(result, error_message= error_message, status = True)

