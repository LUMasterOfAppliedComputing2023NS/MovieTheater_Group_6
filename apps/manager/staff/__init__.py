from flask import Blueprint, render_template, request, url_for, redirect
from werkzeug.security import generate_password_hash, check_password_hash
from db.models import User

manager_staff_bp = Blueprint('manager_staff', __name__)


@manager_staff_bp.route('/', methods=['GET', 'POST'])
def index():

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
            is_staff=1
        )
        redirect(url_for('manager_staff.index'))
    page = request.args.get('page', 1, type=int)
    size = request.args.get('size', 10, type=int)
    staff = User.get_any(offset=(page - 1) * size, limit=size,where=f'is_staff=true')
    count = User.count(where='is_staff=true')
    pages = count // size if count % size == 0 else count // size + 1
    currentPage = page
    return render_template('manager/staff.html',
                           staff=staff, pages=pages, currentPage=currentPage)


@manager_staff_bp.route('/delete/<int:sid>')
def delete(sid):
    User.delete_by_id(sid)
    return redirect(url_for('manager_staff.index'))


@manager_staff_bp.route('/update', methods=['POST'])
def update():
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
    return redirect(url_for('manager_staff.index'))