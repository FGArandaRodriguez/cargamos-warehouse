#Método de stock, en esta clase se programan las funciones para la api de Inventario/Stock.

#########################################################################################
#importamos las herramientas y modelos a utillizar
from flask_restplus import Namespace, abort, marshal_with, Resource, fields
from database import db
from src.models.items import Item
from src.models.stocks import Stock

service = Namespace('stock', description='API para el control del inventario/Stock de almacenes')

stock = service.model('Stock', {
    'id': fields.Integer(read_only=True, description='Identificador del stock'),
    'warehouse_id': fields.Integer(required=True, description='Identificador del almacén'),
    'item_sku': fields.Integer(required=True, description='SKU del artículo'),
    'minimum_stock': fields.Integer(required=True, description='Stock mínimo'),
    'stock': fields.Integer(required=True, description='Stock real')
})

stock_args = service.parser()
#Definimos los argumentos a utilizar
stock_args.add_argument('warehouse_id', type=int, required=True, help='Identificador del almacén')
stock_args.add_argument('item_sku', type=int, required=True, help='SKU del artículo')
stock_args.add_argument('minimum_stock', type=int, required=True, help='Stock mínimo')
stock_args.add_argument('stock', type=int, required=True, help='Stock real')


#Creamos una función para ligar los artículos con los almacenes 
@service.route('/')
class StockWarehouseMethod(Resource):

    @service.doc(id='create-stock', parser=stock_args)
    @service.marshal_with(stock)
    def post(self):
        """crea un nuevo stock  para un almacen"""
        args = stock_args.parse_args()
        #consultamos el stock de productos de acuerdo a el almacèn
        item_exist = db.session.query(Stock).filter(
            Stock.warehouse_id==args['warehouse_id'], 
            Stock.item_sku==args['item_sku']
        ).first()
        
        #validamos que no se inserte un mismo nombre de artìculo en un mismo almacèn
        if item_exist:
            abort(404, message=f'El artìculo   ya se encuentra registrado en el inventario del almacen.')
        
        stock = Stock(warehouse_id = args['warehouse_id'],
            item_sku = args['item_sku'],
            minimum_stock = args['minimum_stock'],
            stock = args['stock']
        )
        db.session.add(stock)
        db.session.commit()
        
        return stock, 201
