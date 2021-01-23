from database import db
#Tabla/Modelo de articulos, aqui se guardarán los artículos disponibles

class Item(db.Model):
    __tablename__ = 'items'
    sku = db.Column(db.Integer, primary_key=True)
    item = db.Column(db.String(255))
    stocks = db.relationship('Stock', backref='item', lazy=True)