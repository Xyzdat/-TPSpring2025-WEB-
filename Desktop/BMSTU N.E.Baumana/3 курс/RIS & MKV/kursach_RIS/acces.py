from flask import session, redirect, flash, url_for, current_app ,request
from functools import wraps

db_access = {
    "worker" : ["main_workers"],
    "manager": ["main_workers","get_category", "request_result", "show_couriers", "report", "create_report"],
    "seller": ["main_workers", "seller", "save_couriers"],
    "courier": ["main_workers", "courier_ord"],
    "user": ["auth_bp", "shop_bp"],
    "director": ["main_workers","report","get_category", "request_result"],
    "buhgalter": ["main_workers","get_category", "request_result", "report", "create_report"]
}

def login_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if 'username' not in session:
            flash("Please log in to access this page.")
            return redirect(url_for('auth_bp.login'))
        return func(*args, **kwargs)
    return wrapper

def group_required(func):

    @wraps(func)
    def wrapper(*args, **kwargs):
        if 'user_group' in session:
            user_role = session.get('user_group')
            print(user_role)
            user_request = request.endpoint
            print('request_endpoint=', user_request)
            user_bp = user_request.split('.')[0]
            user_bp_end = user_request.split('.')[1]
            access = db_access
            if user_bp_end:
                if user_role in access and  user_bp_end in access[user_role]:
                    return func(*args, **kwargs)
            if user_bp:
                print(user_bp)
                print(access[user_role])    
                if user_role in access and user_bp in access[user_role]:
                    return func(*args, **kwargs)
                else:
                    return 'У вас нет прав'
            else:
                return 'У вас нет прав'
        else:
            return redirect(url_for('shop_bp.main_shop'))
    return wrapper