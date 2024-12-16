from dataclasses import dataclass
from database.reqst import select_string, select

@dataclass
class ProductInfoRespronse:
    result: tuple
    error_message: str
    status: bool

def model_route_report(db_config, user_input_data, sql_provider):
    error_message = ''
    _sql = sql_provider.get('procedure_rep.sql',input_month = user_input_data['month'], input_year=user_input_data['year'])
    result, schema = select(db_config, _sql)
    if result or schema:
        return ProductInfoRespronse(result, error_message=error_message, status=True)
    return ProductInfoRespronse(result, error_message=error_message, status=False)