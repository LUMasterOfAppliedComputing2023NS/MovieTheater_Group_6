import datetime
from flask import Blueprint, render_template, request, redirect, url_for, g
from werkzeug.security import generate_password_hash

from db.models import User

admin_bp = Blueprint('admin', __name__)


@admin_bp.route('/account')
def account_index():
    return render_template('admin/account/index.html')


@admin_bp.route('/staff')
def account_staff():
    return redirect(url_for('manager_staff.index'))


@admin_bp.route('/customer')
def account_customer():
    if request.method == 'POST':
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        email = request.form['email']
        address = request.form['address']
        password = request.form['password']
        User.create(
            first_name=first_name,
            last_name=last_name,
            email=email,
            address=address,
            pass_hash=generate_password_hash(password)
        )
        redirect(url_for('manager_staff.index'))
    page = request.args.get('page', 1, type=int)
    size = request.args.get('size', 10, type=int)
    customers = User.get_any(offset=(page - 1) * size, limit=size, where='is_staff=0 and is_admin=0 and is_manager=0')
    count = User.count(where='is_staff=true')
    pages = count // size if count % size == 0 else count // size + 1
    currentPage = page
    return render_template('admin/account/customer.html', customers=customers,
                           pages=pages, currentPage=currentPage)


@admin_bp.route('/customer/delete/<int:sid>')
def customer_delete(sid):
    User.delete_by_id(sid)
    return redirect(url_for('admin.account_customer'))


@admin_bp.route('/customer/update', methods=['POST'])
def customer_update():
    id = request.form['id']
    first_name = request.form['first_name']
    last_name = request.form['last_name']
    email = request.form['email']
    address = request.form['address']
    password = request.form['password']
    User.update_by_id(id=id,
                      first_name=first_name,
                      last_name=last_name,
                      email=email,
                      address=address,
                      pass_hash=generate_password_hash(password))
    return redirect(url_for('admin.account_customer'))


@admin_bp.route('/manager')
def account_manager():
    if request.method == 'POST':
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        email = request.form['email']
        address = request.form['address']
        password = request.form['password']
        User.create(
            first_name=first_name,
            last_name=last_name,
            email=email,
            address=address,
            pass_hash=generate_password_hash(password),
            is_manage=1
        )
        redirect(url_for('manager_staff.index'))
    page = request.args.get('page', 1, type=int)
    size = request.args.get('size', 10, type=int)
    managers = User.get_any(offset=(page - 1) * size, limit=size, where='is_manager=1')
    count = User.count(where='is_staff=true')
    pages = count // size if count % size == 0 else count // size + 1
    currentPage = page
    return render_template('admin/account/manager.html', managers=managers,
                           pages=pages, currentPage=currentPage)


@admin_bp.route('/manager/delete/<int:sid>')
def manager_delete(sid):
    User.delete_by_id(sid)
    return redirect(url_for('admin.account_manager'))


@admin_bp.route('/manager/update', methods=['POST'])
def manager_update():
    id = request.form['id']
    first_name = request.form['first_name']
    last_name = request.form['last_name']
    email = request.form['email']
    address = request.form['address']
    password = request.form['password']
    User.update_by_id(id=id,
                      first_name=first_name,
                      last_name=last_name,
                      email=email,
                      address=address,
                      pass_hash=generate_password_hash(password))
    return redirect(url_for('admin.account_manager'))


@admin_bp.route('/movie')
def movie():
    return redirect(url_for('manager_movie.index'))


@admin_bp.route('/promotion')
def promotion():
    return redirect(url_for('manager_promotion.index'))


@admin_bp.route('/report')
def report():
    return redirect(url_for('manager_report.index'))


@admin_bp.route('/contractUs', methods=['GET', 'POST'])
def contractUs():
    start_time = g.get('start_time')
    end_time = g.get('end_time')
    address = g.get('address')
    phone = g.get('phone')
    if request.method == 'POST':
        start_time = request.form['start_time']
        end_time = request.form['end_time']
        phone = request.form['phone']
        address = request.form['address']
        g.setdefault('start_time', start_time)
        g.setdefault('end_time', end_time)
        g.setdefault('phone', phone)
        g.setdefault('address',address)
    return render_template('admin/contractUs.html',
                           start_time=start_time, end_time=end_time, phone=phone, address=address)


@admin_bp.post('create_account')
def create_account():
    body = request.form.to_dict()
    is_staff = body.get('is_staff', False)
    is_manager = body.get('is_manager', False)
    url_role = 'admin.account_customer'
    if is_staff:
        url_role = 'admin.account_staff'
    if is_manager:
        url_role = 'admin.account_manager'
    date_joined = datetime.date.today().strftime('%Y-%m-%d')
    print(body)
    User.create(**body, date_joined=date_joined)
    return redirect(url_for(url_role))
