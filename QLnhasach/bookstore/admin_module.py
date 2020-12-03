from bookstore import admin, db
from bookstore.models import TacGia, TheLoai, KeSach, Sach
from flask_admin.contrib.sqla import ModelView

admin.add_view(ModelView(TacGia, db.session))
admin.add_view(ModelView(TheLoai, db.session))
admin.add_view(ModelView(Sach, db.session))