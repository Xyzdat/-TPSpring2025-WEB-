from flask import render_template, Flask, session, request, redirect, url_for, flash, Blueprint, json
import os
from database.db_conect import db_config, DBConnection
from query.route import  query_blueprint
from shop.routes import shop_blueprint
from report.route import report_blueprint
from forms import OrderForm
from auth import auth_blueprint
from database.reqst import select
from database.sql_provider import SQLprovider
from acces import login_required, group_required

app = Flask(__name__)

with open("data/db_acces.json") as f:
    app.config['db_acces'] = json.load(f)

app.register_blueprint(auth_blueprint, url_prefix='/auth')
app.register_blueprint(query_blueprint, url_prefix='/query')
app.register_blueprint(shop_blueprint, url_prefix='/shop')
app.register_blueprint(report_blueprint,url_prefix='/report')

sql_provider = SQLprovider(os.path.join(os.path.dirname(__file__), 'sql'))
app.secret_key = 'you_will_nevwr_guess'

@app.route('/')
@login_required
def main():
    print(session['user_group'])
    if session['user_group'] == 'worker' or session['user_group'] == 'courier' or session['user_group'] == 'manager' or  session['user_group'] == 'seller' :
        return redirect(url_for('query_bp.main_workers'))
    return redirect(url_for('shop_bp.main_shop'))