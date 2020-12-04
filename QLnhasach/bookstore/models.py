from sqlalchemy import Column, Integer, Float, String, Date, ForeignKey, Boolean
from sqlalchemy import Table
from sqlalchemy.orm import relationship
from bookstore import db

class QuyenUser(db.Model):
    __tablename__ = 'quyenuser'

    id = Column(Integer, primary_key=True, autoincrement=True)
    tenquyen = Column(String(20), nullable=False)
    loaiquyen = Column(Integer, nullable=False)

class TaiKhoan(db.Model):
    __tablename__ = 'taikhoan'

    id = Column(Integer, primary_key=True, autoincrement=True)
    email = Column(String(30), unique=True, nullable=False)
    matkhau = Column(String(32), nullable=False)
    trangthai = Column(Boolean, nullable=False)

    def __str__(self):
        return self.email


class KhachHang(db.Model):
    __tablename__ = 'khachhang'

    id = Column(Integer, primary_key=True, autoincrement=True)
    email = Column(String(50), ForeignKey(TaiKhoan.email), nullable=False)
    hoten = Column(String(50), nullable=False)
    diachi = Column(String(255), nullable=True)
    sodienthoai = Column(String(10), nullable=False)
    sotienno = Column(Float, default= 0, nullable=False)

    def __str__(self):
        return self.email, self.hoten

class TacGia(db.Model):
    __tablename__ = 'tacgia'

    matacgia = Column(Integer, primary_key=True, autoincrement=True)
    tentacgia = Column(String(50), nullable=False)
    ngaysinh = Column(Date, nullable=True)
    ngaymat = Column(Date, nullable=True)
    quequan = Column(String(100), nullable=True)
    Sach = relationship('Sach', backref='TacGia', lazy=True)

    def __str__(self):
        return self.tentacgia

class TheLoai(db.Model):
    __tablename__ = 'theloai'

    matheloai = Column(Integer, primary_key=True, autoincrement=True)
    tentheloai = Column(String(100), nullable=False)
    ngaythem = Column(Date, nullable= True)
    Sach = relationship('Sach', backref='TheLoai', lazy=False)

    def __str__(self):
        return self.tentheloai

class Sach(db.Model):
    __tablename__ = 'sach'

    masach = Column(Integer, primary_key=True, autoincrement=True)
    tensach = Column(String(50), unique=True, nullable=False)
    theloai = Column(Integer, ForeignKey(TheLoai.matheloai))
    tacgia = Column(Integer, ForeignKey(TacGia.matacgia))
    dongia = Column(Float, default=0, nullable=False)
    soluongton = Column(Integer, default=0, nullable=False)
    image = Column(String(255), nullable=True)

    def __str__(self):
        return self.masach, self.tensach

class Tacgia_Sach(db.Model):
    __tablename__ = 'tacgia_sach'

    tacgia = Column(Integer, ForeignKey(TacGia.matacgia), nullable=False, primary_key=True)
    sach = Column(Integer, ForeignKey(Sach.masach), nullable=False, primary_key=True)

    def __str__(self):
        return self.tacgia, self.sach

class HoaDon(db.Model):
    __tablename__ = 'hoadon'

    mahoadon= Column(Integer, primary_key=True, nullable=False)
    ngaynhap= Column(Date, nullable=True)
    tongtien = Column(Float, default=0)

    def __str__(self):
        return self.mahoadon

class ChiTietHoaDon(db.Model):
    __tablename__ = 'chitiethoadon'

    mahoadon = Column(Integer, ForeignKey(HoaDon.mahoadon), primary_key=True)
    masach = Column(Integer, ForeignKey(Sach.masach))
    soluongban = Column(Integer, default=0, nullable=False)
    giaban = Column(Float, nullable=False, )

    def __str__(self):
        return self.mahoadon, self.masach

class PhieuNhap(db.Model):
    __tablename__ = 'phieunhap'

    maphieunhap = Column(Integer, primary_key=True)
    ngaynhap = Column(Date, nullable=True)

class ChiTietPhieuNhap(db.Model):
    __tablename__ = 'chitietphieunnhap'

    maphieunhap = Column(Integer, ForeignKey(PhieuNhap.maphieunhap), primary_key=True)
    soluongnhap = Column(Integer, default=0)
    masach = Column(Integer, ForeignKey(Sach.masach), nullable=True)

class PhieuThuTien(db.Model):
    __tablename__ = 'phieuthutien'

    maphieuthu = Column(Integer, primary_key=True, autoincrement=True)
    makhachhang = Column(Integer, ForeignKey(KhachHang.id))
    ngaythu = Column(Date, nullable=True)
    sotienthu = Column(Float, default=0, nullable=False)

    def __str__(self):
        self.maphieuthu

if __name__ == '__main__':
    db.create_all()


