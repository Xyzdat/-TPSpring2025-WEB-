from flask import Blueprint, render_template, request, session, flash, redirect, url_for
from forms import LoginForm, RegistrationForm
from .model_route import model_route_auth_req_user, model_route_auth_req_worker, model_route_check, model_route_reg, model_route_auth_req_courier
import os
from . import auth_blueprint
from database.db_conect import db_config, DBConnection
from database.reqst import select
from database.sql_provider import SQLprovider

sql_provider = SQLprovider(os.path.join(os.path.dirname(__file__),'sql'))

@auth_blueprint.route('/login', methods = ['GET', 'POST'])
def login():
    form = LoginForm()
    if request.method == 'GET':
        return render_template('login.html', form = form)
    else:
        user_data = request.form
        user_group_form = request.form['roleHidden']
        if user_group_form == 'user': 
            res_info = model_route_auth_req_user(db_config, user_data, sql_provider)
            print(res_info.result)
            if not res_info.status:
                flash('Ошибка')
                return redirect(url_for('auth_bp.login'))
            elif not res_info.result:
                flash('Ошибка')
                return redirect(url_for('auth_bp.login'))
            user_group = res_info.result[0][6]
        if user_group_form == 'worker':
            res_info = model_route_auth_req_worker(db_config, user_data, sql_provider)
            if not res_info.status:
                flash('Ошибка')
                return redirect(url_for('auth_bp.login'))
            elif not res_info.result:
                flash('Ошибка')
                return redirect(url_for('auth_bp.login'))
            user_group = res_info.result[0][4]
        # if user_group != 'courier':
        #     res_info = model_route_auth_req_courier(db_config, user_data, sql_provider)
        #     if not res_info.status:
        #         flash('Ошибка')
        #         return redirect(url_for('auth_bp.login'))
        #     elif not res_info.result:
        #         flash('Ошибка')
        #         return redirect(url_for('auth_bp.login'))
        #     user_group = "courier"
        username = res_info.result[0][1]
        user_id = res_info.result[0][0]
        session['user_id'] = user_id
        session['user_group'] = user_group
        print(user_group)
        session['username'] = username
        if user_group_form == 'worker':
            return redirect(url_for('query_bp.main_workers'))
        if user_group == 'user':
            return redirect(url_for('shop_bp.main_shop'))
        if user_group_form == 'worker':
            return redirect(url_for('query_bp.main_workers'))
        if user_group == 'courier':
            return redirect(url_for('query_bp.main_workers'))
    
@auth_blueprint.route('/logout')
def logout():
    session.clear()
    return  redirect(url_for('auth_bp.login'))

@auth_blueprint.route('/registr',  methods = ['GET', 'POST'])
def register():
    form = RegistrationForm()
    if request.method == 'GET':
        return render_template('register.html', form = form)
    else:
        user_data = request.form
        password = form.password.data
        password2 = form.password2.data
        res_info = model_route_check(db_config, user_data, sql_provider)
        if not res_info.status:
            flash('Такой пользователь уже есть')
            return redirect(url_for('auth_bp.login'))
        if res_info.result:
            flash('Такой пользователь уже есть')
            return redirect(url_for('auth_bp.register'))
        
        res_info_reg = model_route_reg(db_config, user_data, sql_provider)
        if not res_info_reg.status:
            flash('Ошибка')
            return redirect(url_for('auth_bp.register'))
        flash('Вы успешно зарегистрировались!')
        return redirect(url_for('auth_bp.login'))
    # if form.validate_on_submit():
    #     username = form.username.data
    #     password = form.password.data
    #     email = form.email.data
    #     with DBConnection(db_config) as cursor:
    #         user_check = "SELECT * from user where username=%s or email=%s "
    #         cursor.execute(user_check, (username, email))
    #         current_user = cursor.fetchall()
    #         if current_user: 
    #             flash('пользователь уже есть, используйте другое имя')
    #             return redirect(url_for('auth_bp.register'))
    #         user_insert = "INSERT INTO user(username, email, password) VALUES (%s, %s, %s)"
    #         cursor.execute(user_insert, (username, email, password))
    #         flash('Вы успешно зарегистрировались!')
    #         return redirect(url_for('auth_bp.login'))
    # return render_template('register.html', form = form)