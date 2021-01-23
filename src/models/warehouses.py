#Tabla/Modelo de almacenes, (almacenes o tiendas)
from database import db

class Warehouse(db.Model):
    __tablename__ = 'warehouses'
    id = db.Column(db.Integer, primary_key=True)
    warehouse = db.Column(db.String(255))
    address = db.Column(db.String(255))
    stocks = db.relationship('Stock', backref='warehouse', lazy=True)
