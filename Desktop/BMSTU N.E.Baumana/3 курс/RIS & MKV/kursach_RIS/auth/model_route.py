from dataclasses import dataclass
from database.reqst import select_string
import hashlib

@dataclass
class ProductInfoRespronse:
    result: tuple
    error_message: str
    status: bool

def myhash(text):
    return hashlib.sha256(text.encode()).hexdigest()

def model_route_auth_req_user(db_config, user_input_data, sql_provider):
    error_message = ''
    _sql = sql_provider.get('user.sql', username = user_input_data['username'], password=user_input_data['password'])
    result, schema = select_string(db_config, _sql)
    if result or schema:
        return ProductInfoRespronse(result, error_message=error_message, status=True)
    return ProductInfoRespronse(result, error_message=error_message, status=False)

def model_route_auth_req_worker(db_config, user_input_data, sql_provider):
    error_message = ''
    _sql = sql_provider.get('worker.sql', username = user_input_data['username'], password=user_input_data['password'])
    result, schema = select_string(db_config, _sql)
    if result or schema:
        return ProductInfoRespronse(result, error_message=error_message, status=True)
    return ProductInfoRespronse(result, error_message=error_message, status=False)

def model_route_auth_req_courier(db_config, user_input_data, sql_provider):
    error_message = ''
    _sql = sql_provider.get('courier.sql', username = user_input_data['username'], password=user_input_data['password'])
    result, schema = select_string(db_config, _sql)
    print(result)
    if result or schema:
        return ProductInfoRespronse(result, error_message=error_message, status=True)
    return ProductInfoRespronse(result, error_message=error_message, status=False)



def model_route_check(db_config, user_input_data, sql_provider):
    error_message = ''
    sql = sql_provider.get('check_user.sql', username = user_input_data['username'], email = user_input_data['email'])
    result, schema = select_string(db_config, sql)
    if result or schema:
        return ProductInfoRespronse(result, error_message=error_message, status=True)
    return ProductInfoRespronse(result, error_message=error_message, status=False)

def model_route_reg(db_config, user_input_data, sql_provider):
    error_message = ''
    sql = sql_provider.get('register.sql', 
                            username = user_input_data['username'],
                            password = user_input_data['password'],
                            user_group = 'user',
                            email = user_input_data['email']
                            )
    result = select_string(db_config, sql)
    if result:
        return ProductInfoRespronse(result, error_message=error_message, status=True)
    return ProductInfoRespronse(result, error_message=error_message, status=False)