from flask import Blueprint, render_template, request, session, flash, redirect, url_for, jsonify
from forms import OrderForm
from rembg import remove
from database.db_conect import db_config, DBConnection
from database.reqst import select, select_insert_ord, select_id
from database.sql_provider import SQLprovider
from acces import login_required, group_required
from .model_route import model_route_order_id, model_route_order_item, model_route_order_sel, model_route_order
import os
import json

sql_provider = SQLprovider(os.path.join(os.path.dirname(__file__), 'sql'))

shop_blueprint = Blueprint('shop_bp', __name__, template_folder='templates')

@shop_blueprint.route('/')
@login_required
@group_required
def main_shop():
    flowers = select(db_config, 'SELECT * FROM bunchs')
    cart  = session.get('cart', [])
    if flowers is None:
        return 'Цыетов нету'
    else:
        return render_template('main.html', flowers = flowers, cart = cart)

            
            # <!-- </form> -->        
            # # <!-- <form action="{{ url_for('shop_bp.add_to_cart', flower_id = flower[0])}} " method="post"> -->

# @shop_blueprint.route('/add_to_cart/<int:flower_id>', methods=['POST'])
# @group_required
# def add_to_cart(flower_id):
#     if 'username' not in session:
#         flash('Чтобы добавлять товары в корзину вам необходимо войти в аккаунт или зарегистрироваться')
#         return redirect(url_for('main'))
    
#     flower = select(db_config, sql_provider.get('cart_items.sql', b_id = flower_id))
#     if flower:
#         if 'cart' not in session:
#             session['cart'] = []
#         session['cart'].append({
#                 'b_id': flower[0][0],
#                 'b_cost': flower[0][1],
#                 'b_name': flower[0][2],
#                 'img_src':flower[0][3],
#                 'quantity': 1
#             })
#         session.modified = True
#     return redirect(url_for('shop_bp.main_shop'))

@shop_blueprint.route('/cart',  methods=['GET','POST'])
@group_required
@login_required
def cart():
    cart = session.get('cart', [])
    total_sum = sum(item['b_cost'] for item in cart)
    return render_template('cart.html', total_sum = total_sum,cart=cart)

# <form action="{{ url_for('shop_bp.remove_from_cart', flower_id = cart['b_id'])}}" method="post">
# </form>

# @shop_blueprint.route('/remove_from_cart/<int:flower_id>', methods=['POST'])
# @group_required
# @login_required
# def remove_from_cart(flower_id):
#     cart = session.get('cart', [])
#     cart = [item for item in cart if item['b_id'] != flower_id]
#     session['cart'] = cart
#     session.modified = True
#     return redirect(url_for('shop_bp.cart'))

@shop_blueprint.route('/order', methods = ['GET','POST'])
@group_required
@login_required
def order():
    user_id = session.get('user_id')
    print(user_id)
    cart = session.get('cart', [])
    total_sum = sum(item['b_cost'] for item in cart)
    # form = OrderForm()
    # if form.validate_on_submit():
    if request.method == 'POST':
        date = request.form.get('date')
        adres = request.form.get('adres')
        # date = date.split('T')
        print(date, adres)
        user_data = request.form
        res_info_res = model_route_order(db_config, user_data, sql_provider, date, adres)
        # order_id = res_info_res.result
        # print(order_id)
        if not res_info_res.status:
            flash('Ошибка')
            return redirect(url_for('shop_bp.order'))
        elif not res_info_res.result:
            flash('Ошибка')
            return redirect(url_for('shop_bp.order'))
        else:
        #     for item in cart:
        #         res_info_ins_item = model_route_order_item(db_config,item,sql_provider,order_id)
        #         print(res_info_ins_item.result)
        #         if not res_info_ins_item.status:
        #             flash('Ошибка')
        #             return redirect(url_for('shop_bp.order'))
        #         elif not res_info_ins_item.result:
        #             flash('Ошибка')
        #             return redirect(url_for('shop_bp.order'))
            
            session.pop('cart', None)
            return redirect(url_for('shop_bp.order'))
    return render_template('order.html', total_sum = total_sum)

@shop_blueprint.route('/update_cart_quantity', methods=['POST'])
@group_required
@login_required
def update_cart_quantity():
    cart = session.get('cart', [])
    data = request.get_json()
    item_id = data.get('item_id')
    new_quantity = data.get('quantity')
    print(f"Обновление: ID товара - {item_id}, новое количество - {new_quantity}")
    for item in cart:
        if str(item['b_id']) == str(item_id):
            item['quantity'] = new_quantity
            break

    session['cart'] = cart

    total_sum = sum(item['b_cost'] * item['quantity'] for item in cart)
    session['total_sum'] = total_sum
    return jsonify({'success': True, 'total_sum':total_sum})


@shop_blueprint.route('/add_to_order_btn', methods=['POST'])
@group_required
@login_required
def add_to_order_btn():
    data = request.get_json()
    item_id = data.get('item_id')
    print(item_id)
    flower = select(db_config, sql_provider.get('cart_items.sql', b_id = item_id))
    if flower:
        if 'cart' not in session:
            session['cart'] = []
        session['cart'].append({
                'b_id': flower[0][0],
                'b_cost': flower[0][1],
                'b_name': flower[0][2],
                'img_src':flower[0][3],
                'quantity': 1
            })
        session.modified = True
    session['message_after_insert'] = '✔ В корзине'
    cart = session.get('cart', [])
    total_sum = sum(item['b_cost'] * item['quantity'] for item in cart)
    session['total_sum'] = total_sum
    return jsonify({'success': True, 'message_after_insert':session['message_after_insert'],'total_sum': total_sum})


@shop_blueprint.route('/remove_from_cart', methods=['POST'])
@group_required
@login_required
def remove_from_cart():
    data = request.get_json()
    item_id = data.get('item_id')
    cart = session.get('cart', [])
    cart = [item for item in cart if str(item['b_id']) != str(item_id)]
    session['cart'] = cart
    session.modified = True
    total_sum = sum(item['b_cost'] * item['quantity'] for item in cart)
    if (total_sum == 0):
        session.pop('cart')
    session['total_sum'] = total_sum
    return jsonify({'success': True, 'total_sum': total_sum})

@shop_blueprint.route('/', methods = ['POST'])
@group_required
@login_required
def search_flowers():
    flower_name = request.form
    flower = select(db_config, sql_provider.get('flower.sql', flower_name = flower_name['flower_name']))
    return render_template('main.html', flowers = flower)

@shop_blueprint.route('/my_orders' )
@group_required
@login_required
def my_orders():
    user_id = session.get('user_id')
    results = []
    order_id = model_route_order_id(db_config, user_id, sql_provider)
    sql_template =  """select o_id ,client_order.cost, client_order.delivery_date, bunchs.b_name, bunchorder.quantiti from bunchorder
                join bunchs using (b_id)
                join client_order on client_order.o_id = bunchorder.order_id
                where client_order.client_id = %s and client_order.o_id = %s"""
    print(order_id.result)
    # with DBConnection(db_config) as cursor:
    #     if cursor is None:
    #         return "NO"
    #     else:
    for ord_id in order_id.result:
        my_order = select(db_config, sql_provider.get('my_order.sql', user_id = user_id))
                # cursor.execute(sql_template, (user_id, ord_id))
                # result = cursor.fetchall()
                # results.extend(result)
                # print(results)
    # flower = select(db_config, sql_provider.get('flower_in_order.sql', user_id = user_id, order_id = result[0]))
    return render_template('my_orders.html', my_orders= my_order)