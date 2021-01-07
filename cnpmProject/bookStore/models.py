from bookStore import db
from sqlalchemy import Table, Column, ForeignKey, Enum
from sqlalchemy import Integer, Float, String, Boolean, Date
from sqlalchemy.orm import relationship
from enum import Enum as UserEnum
from flask_login import UserMixin

class BookBase(db.Model):
    __abstract__ = True

    id = db.Column(Integer, primary_key=True, autoincrement=True)
    fullname = db.Column(String(100), nullable=False)

    def __str__(self):
        return self.fullname

class Author(BookBase):
    __tablename__ = 'author'

    address = db.Column(String(100), nullable=True)

    def __init__(self,fullname, address):
        self.fullname = fullname
        self.address = address

    def __str__(self):
        return self.fullname

class BookCategory(BookBase):
    __tablename__ = 'book_category'   # thể loại sách

    book_cate = relationship('Books', backref= 'book_category', lazy = True)

    def __init__(self, fullname):
        self.fullname = fullname

    def __str__(self):
        return self.fullname

class Books(BookBase):
    __tablename__ = 'books'  # sách

    price = db.Column(Float, default=0)
    quantity = db.Column(Integer, default=0)
    date_add = db.Column(Date, nullable=True)
    images = db.Column(String(255), nullable=True)
    description = db.Column(String(255), nullable=True)
    status = db.Column(Boolean, default=True)
    cate_id = db.Column(Integer, ForeignKey(BookCategory.id), nullable=True)

    re_inventory = relationship('InventoryReportDetail', backref='books', lazy=True)
    receipt_details = relationship('ReceiptDetail', backref='books', lazy=True)
    re_import_details = relationship('BookImportDetail', backref='books', lazy=True)

    def __init__(self,id, fullname, price, quantity,images, description, status, cate_id):
        self.id = id
        self.fullname = fullname
        self.price = price
        self.quantity = quantity
        self.images = images
        self.description = description
        self.status = status
        self.cate_id = cate_id

    def __str__(self):
        return self.fullname

author_book = db.Table('authors_books',
                db.Column('author_id', db.ForeignKey(Author.id), primary_key=True),
                db.Column('cate_id', db.ForeignKey(Books.id), primary_key=True))

book_cate = db.Table('books_cates',
                db.Column('cate_id', db.ForeignKey(BookCategory.id), primary_key=True),
                db.Column('book_id', db.ForeignKey(Books.id), primary_key=True))

class UserRole(UserEnum):
    admin = 0
    employee = 1
    customer = 2

class Users(BookBase, UserMixin):
    __tablename__ = 'users'

    username = db.Column(String(255), unique=True, nullable=False)
    password = db.Column(String(100), nullable=False)
    avatar = db.Column(String(255), nullable=True)
    permission = db.Column(Enum(UserRole), default=UserRole.customer)

    book_import = relationship('BookImport', backref='users', lazy=True)
    re_bill = relationship('Bills', backref='users', lazy=True)

    def __init__(self, fullname, username, password, avatar, permission):
        self.fullname = fullname
        self.username = username
        self.password = password
        self.avatar = avatar
        self.permission = permission

    def __str__(self):
        return self.fullname

    def dislay(self):
        return self.id, self.fullname, self.username, self.permission

class Cutomers(BookBase):
    __tablename__ = 'customers'

    email = db.Column(String(255), unique=True)
    phone = db.Column(String(15), nullable=True)
    address = db.Column(String(255), nullable=True)
    debt = db.Column(Float, default=0)
    status = db.Column(Boolean, default=True)
    user_id = db.Column(Integer, ForeignKey(Users.id), nullable=True)

    re_receipts = relationship('Receipt', backref='customers', lazy=True)
    re_bill = relationship('Bills', backref='customers', lazy=True)
    debt_report_details = relationship('DebtReportDetail', backref='customers', lazy=True)

    def __init__(self,fullname, email, phone, address, debt, status):
        self.fullname = fullname
        self.email = email
        self.phone = phone
        self.address = address
        self.debt = debt
        self.status = status

    def __str__(self):
        return self.fullname

    def dislay(self):
        return self.id, self.fullname, self.email, \
               self.phone, self.address, self.debt, self.status, self.user_id

class Report(db.Model):
    __abstract__ = True

    report_id = db.Column(Integer, primary_key=True, autoincrement=True)
    day = db.Column(Integer, nullable=True)
    month = db.Column(Integer, nullable=True)
    year = db.Column(Integer, nullable=True)

    def __init__(self, day, month, year):
        self.day = day
        self.month = month
        self.year = year

class DebtReport(Report):
    __tablename__ = 'debt_report' # báo cáo nợ

    debt = relationship('DebtReportDetail', backref='debt_report', lazy=True)

    def __str__(self):
        return self.report_id

class DebtReportDetail(db.Model):
    __tablename__ = 'debt_report_detail' # chi tiết báo cáo nợ

    detail_id = db.Column(Integer, primary_key=True, autoincrement=True)
    first_debt = db.Column(Float, nullable=False)
    final_debt = db.Column(Float, nullable=False)
    customer_id = db.Column(Integer, ForeignKey(Cutomers.id))
    debt_id = db.Column(Integer, ForeignKey(DebtReport.report_id), nullable=False)

    def __init__(self, detail_id, first_debt, final_debt, customer_id, debt_id):
        self.detail_id = detail_id
        self.first_debt = first_debt
        self.final_debt = final_debt
        self.customer_id = customer_id
        self.debt_id = debt_id

class InventoryReport(Report):
    __tablename__ = 'inventory_report' # báo cáo tồn

    inventory = relationship('InventoryReportDetail', backref='inventory_report', lazy=True)

class InventoryReportDetail(db.Model):
    __tablename__= 'inventory_report_detail'  # chi tiết báo cáo tồn

    detail_id = db.Column(Integer, ForeignKey(InventoryReport.report_id), primary_key=True)
    book_id = db.Column(Integer, ForeignKey(Books.id), primary_key=True)
    first_quantity = db.Column(Integer, nullable=False)
    final_quantity = db.Column(Integer, nullable=False)

    def __init__(self, detail_id, book_id, first, final):
        self.detail_id = detail_id
        self.book_id = book_id
        self.first_quantity = first
        self.final_quantity = final


class Receipt(db.Model):
    __tablename__ = 'receipt'

    id = db.Column(Integer, primary_key=True, autoincrement=True)
    create_date = db.Column(Date, nullable=True)
    paid = db.Column(Float, default=0) # số tiền khách trả
    total = db.Column(Float, default=0) # tổng tiền
    customer_id = db.Column(Integer, ForeignKey(Cutomers.id), nullable=True)

    receipts = relationship('ReceiptDetail', backref='receipt', lazy=True)

    def __init__(self, id, date, paid, total, customer):
        self.id = id
        self.create_date = date
        self.paid = paid
        self.total = total
        self.customer_id = customer

class ReceiptDetail(db.Model):
    __tablename__ = 'receipt_detail'

    id = db.Column(Integer, primary_key=True, autoincrement=True)
    receipt_id = db.Column(Integer, ForeignKey(Receipt.id))
    book_id = db.Column(Integer, ForeignKey(Books.id))
    quantity = db.Column(Integer, default=0)
    price = db.Column(Float, default=0)

class BookImport(db.Model):
    __tablename__ = 'book_import'

    id = db.Column(Integer, primary_key=True, autoincrement=True)
    create_date = db.Column(Date, nullable=False)
    employee_id = db.Column(Integer, ForeignKey(Users.id))

    import_details = relationship('BookImportDetail', backref='book_import', lazy=True)

    def __init__(self, id, date, employee):
        self.id = id
        self.create_date = date
        self.employee_id = employee

class BookImportDetail(db.Model):
    __tablename__ = 'book_import_detail'

    id = db.Column(Integer, primary_key=True, autoincrement=True)
    bookimport_id = db.Column(Integer, ForeignKey(BookImport.id))
    book_id = db.Column(Integer, ForeignKey(Books.id))
    quantity = db.Column(Integer, default=0)

    def __init__(self, id, book_import, book_id, quantity):
        self.id = id
        self.bookimport_id = book_import
        self.book_id = book_id
        self.quantity = quantity

class Bills(db.Model):
    __tablename__='bills'   # phiếu thu tiền

    id = db.Column(Integer, primary_key=True, autoincrement=True)
    collect_date = db.Column(Date, nullable=False)  # ngày thu tiền
    proceeds = db.Column(Float, default=0) #số tiền thu
    employee_id = db.Column(Integer, ForeignKey(Users.id))
    customer_id = db.Column(Integer, ForeignKey(Cutomers.id))

    def __init__(self, id, date, money, employee, customer):
        self.id = id
        self.collect_date = date
        self.proceeds = money
        self.employee_id = employee
        self.customer_id = customer

    def __str__(self):
        return self.id

class Policies(BookBase):
    __tablename__ = 'policies'

    quantity = db.Column(Integer, nullable=False)
    status = db.Column(Boolean, default=True)

    def __init__(self, id , name, quantity, status):
        self.id = id
        self.fullname = name
        self.quantity = quantity
        self.status = status

if __name__ == '__main__':
    db.create_all()