from flask import Blueprint, render_template, request, redirect, url_for

from db.models import Coupon

manager_promotion_bp = Blueprint('manager_promotion', __name__)


@manager_promotion_bp.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        title = request.form['title']
        remark = request.form['remark']
        code = request.form['code']
        discount = request.form['discount']
        expiry_date = request.form['expiry_date']
        use_limit = request.form['use_limit']
        Coupon.create(title=title, remark=remark, code=code, discount=discount, expiry_date=expiry_date, used_counter=0,use_limit=use_limit)
    page = request.args.get('page', 1, type=int)
    size = request.args.get('size', 10, type=int)
    coupon = Coupon.get_any(offset=(page - 1) * size, limit=size)
    count = Coupon.count()
    pages = count // size if count % size == 0 else count // size + 1
    currentPage = page
    return render_template('manager/promotion.html', coupon=coupon, pages=pages, currentPage=currentPage)


@manager_promotion_bp.route('/delete/<int:cid>')
def delete(cid):
    Coupon.delete_by_id(cid)
    return redirect(url_for('manager_promotion.index'))


@manager_promotion_bp.route('/update', methods=['POST'])
def update():
    cid = request.form['id']
    title = request.form['title']
    remark = request.form['remark']
    code = request.form['code']
    discount = float(request.form['discount'])
    expiry_date = request.form['expiry_date']
    use_limit = int(request.form['use_limit'])
    Coupon.update_by_id(id=cid,
                        title=title,
                        remark=remark,
                        code=code,
                        discount=discount,
                        expiry_date=expiry_date,
                        use_limit=use_limit)
    return redirect(url_for('manager_promotion.index'))
