from flask import render_template, Flask, request, redirect, url_for, flash, Blueprint, session
from acces import login_required
import os
from database.db_conect import db_config, DBConnection
from database.reqst import select
from database.sql_provider import SQLprovider
from acces import login_required, group_required

query_blueprint = Blueprint('query_bp', __name__, template_folder='templates')

sql_provider = SQLprovider(os.path.join(os.path.dirname(__file__),'sql'))

@query_blueprint.route('/')
@login_required
@group_required
def main_workers():
    return render_template('main_worker.html')

@query_blueprint.route('/order')
@login_required
@group_required
def get_category():
    workers = select(db_config, 'SELECT *  FROM couriers')
    if workers is None:
        return 'Неправильный вход в базу данных'
    else:
        return render_template ('prod_cat.html', workers= workers)

@query_blueprint.route('/order', methods = ['POST'])
@group_required
def request_result():
    user_input = request.form
    workers = select(db_config, sql_provider.get('products.sql', courier_name = user_input['courier_name']))
    prod_title = "Результаты запроса"
    if workers is None:
        return 'Неправильный вход в базу данных'
    else:
        return render_template ('result.html',prod_title = prod_title , workers = workers)

@query_blueprint.route('/couriers')
@login_required
@group_required
def show_couriers():
    return render_template('select_courier.html')

@query_blueprint.route('/couriers',  methods = ['POST'])
def show_couriers_res():
    user_data = request.form
    couriers = select(db_config, sql_provider.get('couriers.sql', courier_name = user_data['courier_name']))
    prod_title = "Результаты запроса"
    if couriers is None:
        return 'Неправильный вход в базу данных'
    else:
        return render_template('select_courier_result.html',prod_title =prod_title,  couriers=couriers)
    
@query_blueprint.route('/courier_ord')
@login_required
@group_required
def courier_ord():
    user_data = session['username']
    courier =  select(db_config, sql_provider.get('courier_ord.sql', username = user_data))
    prod_title = "Ваши заказы"
    if courier is None:
        return 'Неправильный вход в базу данных'
    else:
        return render_template('courier_ord.html',prod_title =prod_title,  couriers=courier)

@query_blueprint.route('/seller', methods = ['GET','POST'])
@login_required
@group_required
def seller():
    if request.method == 'GET':
        return render_template ('seller.html')
    else:
        user_input = request.form
        workers = select(db_config, sql_provider.get('seller.sql', date = user_input['date_seller']))
        couriers = select(db_config, sql_provider.get('seller_courier.sql', date = user_input['date_seller']))
        all_couriers = select(db_config, "select courier_name, courier_id from couriers")
        print (couriers)
        prod_title = "Все заказы по выбраной дате"
        if workers is None:
            return 'Неправильный вход в базу данных'
        else:
            return render_template ('seller_order.html',prod_title = prod_title , workers = workers, couriers = couriers, all_couriers = all_couriers)

@query_blueprint.route('/save_couriers/<int:order_id>', methods=['POST'])
@group_required
@group_required
def save_couriers(order_id):
    couriers = request.form.get('courier')
    print(couriers)
    print(order_id)
    with DBConnection(db_config) as cursor:
        for courier in couriers:
            if courier:
                sql = """
                    UPDATE client_order
                    SET courier_id = %s
                    WHERE o_id = %s
                    """
                cursor.execute(sql, (courier, order_id))
    return redirect(url_for('query_bp.seller'))

# @query_blueprint.route('/seller', methods = ['POST'] )
# @group_required
# def seller_res():
#     user_data = request.form
#     workers = select(db_config, sql_provider.get('seller_insert.sql', courier_id = user_data['courier_name'], o_id =user_data['o_id'] ))
#     if workers is None:
#         return 'Неправильный вход в базу данных'
#     else:
#         return redirect(url_for('query_bp.seller'))