from bookStore import admin, db
from flask_admin.contrib.sqla import ModelView
from flask_admin import BaseView, expose
from flask_login import logout_user, current_user
from bookStore.models import *
from flask import redirect


class AuthenticatedView(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated

class ContactView(BaseView):
    @expose('/')
    def index(self):
        return self.render('admin/contact.html')

class LogoutView(BaseView):
    @expose('/')
    def index(self):
        logout_user()
        return redirect('/admin')

    def is_accessible(self):
        return current_user.is_authenticated

class BookView(ModelView):
    can_create = True
    can_edit = True
    can_export = True
    page_size = 10

class ReceiptView(ModelView):
    can_export = True
    can_edit = True
    can_delete = False
    inline_models = [ReceiptDetail]

# class TestView(BaseView):
#     @expose('/')
#     def __init__(self):
#         return self.render('admin/add_employee.html')





admin.add_view(BookView(Books, db.session))
admin.add_view(ReceiptView(Receipt, db.session))
admin.add_view(ModelView(Cutomers, db.session))

admin.add_view(ContactView(name='About us'))
admin.add_view(LogoutView(name='Đăng xuất'))