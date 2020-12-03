from sqlalchemy import Column, Integer, Float, String, Date, ForeignKey
from sqlalchemy.orm import relationship
from bookstore import db
from flask_sqlalchemy import SQLAlchemy



class TacGia(db.Model):
    __tablename__ = 'tacgia'

    matacgia = Column(Integer, primary_key=True, autoincrement=True)
    tentacgia = Column(String(50), nullable=False)
    ngaysinh = Column(Date, nullable=True)
    ngaymat = Column(Date , nullable=True)
    quequan = Column(String(100), nullable=True)
    #sachs = relationship('sach', backref='tacgia', lazy=False)

    def __str__(self):
        return self.tentacgia

class KeSach(db.Model):
    __tablename__ = 'kesach'

    make = Column(Integer, primary_key=True, autoincrement=True)
    chatlieu = Column(String(50), nullable= True)
    succhua = Column(Integer, nullable= True)

class TheLoai(db.Model):
    __tablename__ = 'theloai'

    matheloai = Column(Integer, primary_key=True, autoincrement=True)
    tentheloai = Column(String(100), nullable=False)
    ngaythem = Column(Date, nullable= True)
    #sachs = relationship('sach', backref='theloai', lazy=False)
    def __str__(self):
        return self.tentheloai

class Sach(db.Model):
    __tablename__ = 'sach'

    masach = Column(String(20), primary_key=True)
    tensach = Column(String(50), unique=True)
    theloai = Column(Integer, ForeignKey(TheLoai.matheloai))
    tacgia = Column(Integer, ForeignKey(TacGia.matacgia))
    kesach = Column(Integer, ForeignKey(KeSach.make))
    dongia = Column(Float, default=0)
    soluongton = Column(Integer, default=0)
    #image = Column(String(255), nullable= True)

    def __str__(self):
        return self.tensach


if __name__ == '__main__':
    db.create_all()



