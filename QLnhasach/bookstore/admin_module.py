from bookstore import admin, db
from bookstore.models import TacGia, TheLoai, Sach, HoaDon, KhachHang, PhieuNhap, PhieuThuTien, ChiTietHoaDon
from flask_admin.contrib.sqla import ModelView

class KhachhangModelView(ModelView):
    column_display_pk = True

class SachModelView(ModelView):
    column_display_pk = True
    can_create = True
    can_edit = True
    can_delete = True
    can_export = True
    # form_columns = ('masach', 'tensach', 'dongia', 'soluongton', 'tacgia', 'theloai', 'kesach', )
    # column_display_all_relations = True

class TacgiaModelView(ModelView):
    column_display_pk = True
    can_create = True
    can_edit = True
    can_delete = True
    can_export = True
    form_columns = ('tentacgia', 'ngaysinh', 'ngaymat', 'quequan', )

class TheloaiModelView(ModelView):
    column_display_pk = True


class HoaDonModelView(ModelView):
    column_display_pk = True

admin.add_view(KhachhangModelView(KhachHang, db.session))
admin.add_view(TacgiaModelView(TacGia, db.session))
admin.add_view(TheloaiModelView(TheLoai, db.session))
admin.add_view(SachModelView(Sach, db.session))

admin.add_view(HoaDonModelView(HoaDon, db.session))
# admin.add_view(ModelView(PhieuThuTien, db.session))
# admin.add_view(ModelView(PhieuNhap, db.session))
