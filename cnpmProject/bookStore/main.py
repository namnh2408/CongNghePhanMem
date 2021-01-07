from flask import render_template, request, redirect, session, url_for, jsonify, json
from bookStore import models, utils, decorator
from bookStore.admin import *
from bookStore import app, login
import os
from flask_login import login_user, current_user, logout_user


categories = utils.getAllCategory()

@app.route('/')
def index():
    products = models.Books.query.filter( models.Books.date_add > '2020-12-21')

    return render_template('index.html', categories=categories, products=products)


# @app.route('/login_admin', methods=['post', 'get'])
# def login_admin():
#     if request.method == 'POST':
#         username = request.form.get('username')
#         password = request.form.get('password', '')
#
#         admin = utils.check_login(username=username,password=password, role=UserRole.admin)
#         if admin:
#             login_user(user=admin)
#
#     return redirect('/admin')

@app.route('/login', methods=['get','post'])
def login_usr():
    msg = ''
    if request.method == 'POST':
        username = request.form.get('uname')
        password = request.form.get('pword')

        user = utils.check_login(username=username,
                                 password=password)
        if user:
            login_user(user=user)
            cate_id = request.args.get('cate_id')
            kw = request.args.get('kw')

            products = utils.search_book(cate_id, kw)

            return render_template('index.html', categories=categories, products=products)
        else:
            msg='Your username or password inccorrect...'
    return render_template('login.html', message=msg, categories=categories)


@app.route('/register', methods=['get', 'post'])
def register():
    err_msg =''
    if request.method == 'POST':
        fname = request.form.get('fullname')
        uname = request.form.get('username')
        email = request.form.get('email')
        phone = request.form.get('phone')
        addr = request.form.get('address')

        # f = request.files['avatar']
        # avatar_path = 'images/upload/%s' % f.filename
        # f.save(os.path.join(app.root_path, 'static/', avatar_path))

        avatar_path = 'images/upload/avatar1.jpg'

        pword = request.form.get('pword')
        repword = request.form.get('repword')

        if pword == repword and uname != '':
            check_user = utils.register_user(fullname=fname,
                                             username= uname, password=pword, avatar=avatar_path)
            check_infor = utils.register_customer(fullname=fname,
                                                  email=email, phone=phone, address=addr)
            if check_user == True and check_infor == True:
                return render_template('login.html', categories=categories)
            else:
                err_msg = 'Hệ thống xảy ra 1 số vấn đề. Vui lòng thực hiện lại...'
        else:
            err_msg = 'Mật khẩu không trùng khớp vui lòng nhập lại...'
    return render_template('register.html', msg= err_msg, categories=categories)

@app.route('/logout')
def logout_page():
    if current_user.is_authenticated:
        logout_user()
    return redirect(url_for('login_usr'))

@app.route('/products')
def product_list():
    cate_id = request.args.get('cate_id')
    kw = request.args.get('kw')

    products = utils.search_book(cate_id, kw)

    counts = utils.countBook(cate_id)
    return render_template('product.html',categories=categories, products=products, counts=counts)


@app.route("/products/?<int:product_id>")
def book_detail(product_id):
    product = utils.getBookById(book_id=product_id)

    return render_template('single.html', categories=categories, product=product)



@app.route('/infomation')
@decorator.login_user_required
def information():
    user = utils.get_info(current_user.fullname)
    return render_template('information.html', categories=categories, info=user)


@app.route('/contact')
def contact():
    return render_template('contact.html', categories=categories)



@app.route('/api/cart', methods=['post'])
def add_to_cart():
    if 'cart' not in session:
        session['cart'] = {}

    cart = session['cart']

    data = json.loads(request.data)

    id = str(data.get("id"))
    fullname = data.get("fullname")
    price = data.get("price", 0)

    if id in cart:
        cart[id]['quantity'] = cart[id]['quantity'] + 1
    else:
        cart[id] = {
            "id": id,
            "fullname": fullname,
            "price": price,
            "quantity": 1
        }

    session['cart'] = cart

    quantity, amount = utils.cart_stats(cart)

    return jsonify({
        "total_quantity": quantity,
        "total_amount": amount
    })


@app.route('/payment')
def payment():
    quantity, amount = utils.cart_stats(session.get('cart'))
    cart_info = {
        "total_quantity": quantity,
        "total_amount": amount
    }
    return render_template('payment.html', cart_info=cart_info, categories=categories)


@app.route('/api/pay', methods=['post'])
@decorator.login_user_required
def pay():
    if utils.add_receipt(session.get('cart')):
        del session['cart']

        return jsonify({
            "message": "Add receipt successful!",
            "err_code": 200
        })

    return jsonify({
        "message": "Failed"
    })


@login.user_loader
def get_user(user_id):
    return utils.get_user_by_id(user_id=user_id)


if __name__ == '__main__':
    app.run(debug=True, port=5000)


