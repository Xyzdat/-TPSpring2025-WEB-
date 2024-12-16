from dataclasses import dataclass
from database.reqst import select_id, select_string, select_insert, select_insert_ord, select
import hashlib
from flask import session
from database.db_conect import DBConnection

@dataclass
class ProductInfoRespronse:
    result: tuple
    error_message: str
    status: bool

@dataclass
class ProductInfoRespronseORD:
    result: int
    error_message: str
    status: bool

def model_route_order_id(db_config, user_id, sql_provider):
    error_message = ''
    # total_sum = session['total_sum']
    sql = sql_provider.get('order_id.sql', 
                            user_id = user_id
                            )
    result = select_id(db_config, sql)
    if result:
        return ProductInfoRespronseORD(result, error_message=error_message, status=True)
    return ProductInfoRespronseORD(result, error_message=error_message, status=False)


def model_route_order_sel(db_config, sql_provider):
    error_message = ''
    sql = sql_provider.get('sel_ord.sql')
    result = select_string(db_config, sql)
    if result:
        return ProductInfoRespronse(result, error_message=error_message, status=True)
    return ProductInfoRespronse(result, error_message=error_message, status=False)

def model_route_order_item(db_config, item, sql_provider, order_id):
    error_message = ''
    cart = session.get('cart', [])
    sql = sql_provider.get('order_item_ins.sql', 
                            order_id = order_id,
                            p_id = item['b_id'],
                            quantity = item['quantity'],
                            price = item['b_cost']
                            )
    result = select_insert(db_config, sql)
    if result:
        return ProductInfoRespronseORD(result, error_message=error_message, status=True)
    return ProductInfoRespronseORD(result, error_message=error_message, status=False)

def model_route_order(db_config, user_input_data, sql_provider, date, adres):
    with DBConnection(db_config) as cursor:
        if cursor is None:
            raise ValueError("Cursor not created")
        else:
            cart = session.get('cart', [])
            error_message = ''
            total_sum = session['total_sum']
            sql = sql_provider.get('order.sql', 
                                    user_id = session.get('user_id'),
                                    cost = total_sum,
                                    date = date,
                                    adres = adres
                                    )
            cursor.execute(sql)
            result = cursor.lastrowid
            order_id = result
            if result:
                for item in cart:
                    sql = sql_provider.get('order_item_ins.sql', 
                                            order_id = order_id,
                                            p_id = item['b_id'],
                                            quantity = item['quantity'],
                                            price = item['b_cost']
                                            )
                    cursor.execute(sql)
                    product_resp = ProductInfoRespronseORD(order_id, error_message=error_message, status=True)
        return product_resp
  