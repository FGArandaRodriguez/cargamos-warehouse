from database import db

# Tabla/Modelo pibote warehouse-items
#Aquí se guardará el inventario de productos en cada almacen

class Stock(db.Model):
    __tablename__ = 'stock'
    id = db.Column(db.Integer, primary_key=True)
    warehouse_id = db.Column(db.Integer, db.ForeignKey('warehouses.id'))
    item_sku = db.Column(db.Integer, db.ForeignKey('items.sku'))
    minimum_stock = db.Column(db.Integer)
    stock  = db.Column(db.Integer)