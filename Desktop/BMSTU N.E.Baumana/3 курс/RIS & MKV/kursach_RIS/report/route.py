from flask import render_template, Flask, request, redirect, url_for, flash, Blueprint
from acces import login_required
import os
from .model_route import model_route_report
from database.db_conect import db_config
from database.reqst import select, select_string, select_proc
from database.sql_provider import SQLprovider
from acces import login_required, group_required

report_blueprint = Blueprint('report_bp', __name__, template_folder='templates')

sql_provider = SQLprovider(os.path.join(os.path.dirname(__file__),'sql'))

@report_blueprint.route('/report')
@group_required
@login_required
def report():
    return render_template('report.html')


@report_blueprint.route('/report',  methods = ['POST'])
@login_required
def watch_report():
    user_input_data = request.form
    result = select(db_config, sql_provider.get('procedure_rep.sql',input_month = user_input_data['month'], input_year=user_input_data['year']))
    prod_title = "Result of your request"
    if result is None:
        return 'Неправильный вход в базу данных'
    else:
        return render_template ('res_report.html' , prod_title=prod_title, results = result)
    
@report_blueprint.route('/report_create', methods = ['GET','POST'])
@group_required
@login_required
def create_report():
    if request.method == 'GET':
        return render_template('create_rep.html')
    else:
        user_input_data = request.form
        result = select_proc(db_config, sql_provider.get('create_rep.sql', input_month = user_input_data['month'], input_year=user_input_data['year']))
        print(result)
        if result is None:
            return 'Неправильный вход в базу данных'
        else:
            flash("Вы успешно создали отчёт")
            return render_template ('res_rep_cr.html', results = result )