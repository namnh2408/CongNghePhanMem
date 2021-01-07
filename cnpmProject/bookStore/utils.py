import json, hashlib
from bookStore.models import *
from bookStore import db


def getAllCategory():
    return BookCategory.query.all()

def search_book(cate_id=None, kw=None):
    products = Books.query

    if cate_id:
        products = products.filter(Books.cate_id== cate_id)

    if kw:
        products = products.filter(Books.fullname.contains(kw))

    return products.all()

def getBookById(book_id):
    return Books.query.get(book_id)

def countBook(cate_id=None):
    counts = Books.query

    if cate_id :
        counts = counts.filter_by(cate_id = cate_id).count()
    else:
        counts = counts.count()
    return counts

def check_login(username, password, role=UserRole.customer):
    permiss = get_user(username)
    role = permiss[3]
    password = str(hashlib.md5(password.encode('utf-8')).hexdigest())
    user = Users.query.filter(Users.username == username,
                            Users.password == password,
                             Users.permission == role).first()

    return user


def get_user_by_id(user_id):
    return Users.query.get(user_id)


def register_customer(fullname, email, phone, address):
    cus = Cutomers(fullname=fullname, email=email, phone=phone,
                        address=address,
                        debt=0,
                        status=1)
    try:
        db.session.add(cus)
        db.session.commit()
        return True
    except:
        return False

def register_user(fullname, username, password, avatar):
    password = str(hashlib.md5(password.encode('utf-8')).hexdigest())
    usr = Users( fullname= fullname,
             username=username,
             password=password,
             avatar=avatar,
             permission = UserRole.customer)

    try:
        db.session.add(usr)
        db.session.commit()
        return True
    except:
        return False


def cart_stats(cart):
    total_amount, total_quantity = 0, 0
    if cart:
        for p in cart.values():
            total_quantity = total_quantity + p["quantity"]
            total_amount = total_amount + p["quantity"]*p["price"]

    return total_quantity, total_amount


def add_receipt(cart):
    if cart:
        receipt = Receipt(customer_id=1)
        db.session.add(receipt)

        for p in list(cart.values()):
            detail = ReceiptDetail(receipt=receipt,
                                   product_id=int(p["id"]),
                                   quantity=p["quantity"],
                                   price=p["price"])
            db.session.add(detail)

        try:
            db.session.commit()
            return True
        except Exception as ex:
            print(ex)

    return False

def check_role(uname, role):
    if role == UserRole.admin or role == UserRole.employee:
        ad = Users.query.filter(Users.username == uname, Users.permission == role).first()
        if ad:
            return 1
        else:
            return 0
    return 0

def get_info(fullname):
    user = Cutomers.query.filter(Cutomers.fullname == fullname).first().dislay()
    return user

def get_user(uname):
    user = Users.query.filter(Users.username == uname).first().dislay()
    return user
