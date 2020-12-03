from bookstore import admin, db
from bookstore.models import TacGia, TheLoai, KeSach, Sach
from flask_admin.contrib.sqla import ModelView

class SachModelView(ModelView):
    column_display_pk = False# hien thi
    can_create = True
    can_edit = True
    can_delete = True
    can_export = True
    form_columns = ('masach', 'tensach', 'theloai', 'tacgia', 'kesach', 'dongia', 'soluongton',)



admin.add_view(ModelView(TacGia, db.session))
admin.add_view(ModelView(TheLoai, db.session))
admin.add_view(ModelView(KeSach, db.session))
admin.add_view(SachModelView(Sach, db.session))