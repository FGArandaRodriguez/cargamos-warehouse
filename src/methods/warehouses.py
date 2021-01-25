#Método de almacén, este espacio se programaràn las funciones para los almacenes

#################################################################################
#importamos las herramientas y modelos a utilizar
from flask_restplus import Namespace, abort, marshal_with, Resource, fields
from database import db
from src.models.warehouses import Warehouse
from src.models.stocks import Stock

service = Namespace('warehouses', description = 'API para el control de los almacenes')

#creamos los schemas############################################################
warehouse = service.model('Warehouse', {
    'id': fields.Integer(read_only=True, description='Identificador del almacén'),
    'warehouse': fields.String(required=True, description='Nombre del almacén'),
    'address': fields.String(required=True, description='Dirección del almacén')
})

stock = service.model('Stock', {
    'id': fields.Integer(read_only=True, description='Identificador'),
    'warehouse_id': fields.Integer(required=True, description='Identificador del almacen'),
    'item_sku': fields.Integer(required=True, description='SKU del artìculo'),
    'minimum_stock': fields.Integer(required=True, description='Stock minimo'),
    'stock': fields.Integer(required=True, description='Stock real')
})
#################################################################################

##añadimos los argumentos requeridos##############################################
warehouse_args = service.parser()
warehouse_args.add_argument('warehouse', type=str, required=True, help='Nombre del almacén')
warehouse_args.add_argument('address', type=str, required=True, help='Dirección del almacén')

warehouse_args_update = service.parser()
warehouse_args_update.add_argument('warehouse', type=str, required=True, help='Nombre del almacén')
warehouse_args_update.add_argument('address', type=str, required=True, help='Dirección del almacén')

##################################################################################
#Funciones:#######

#función que muestra los almacenes con stock de un artículo disponible
@service.route('/available_stock/<sku>')
class WarehouseStockAvailableMethod(Resource):
    @service.doc(id='get-warehousesstock-available')
    @service.marshal_with(stock)
    def get(self, sku):
        """Muestra los almacenes con stock de un producto específico"""
        stock = db.session.query(Stock).filter(Stock.item_sku == sku, Stock.stock >= 1).all()
        #si no encontramos stock en los almacenes, lanzamos un mensaje
        if not stock:
            abort(404, message=f'Ningún almacén cuenta con stock del artículo: {sku}')
        return stock
    ################################################################################

#creamos una clase con funciones para poder insertar y listar almacenes:
@service.route('/')
class WarehousesMethod(Resource):
    #función para insertar un almacén 
    @service.doc(id='warehouse-post', parser=warehouse_args)
    @service.marshal_with(warehouse)
    def post(self):
        """Inserta un almacen"""
        args = warehouse_args.parser()
        warehouse = Warehouse(warehouse = args['warehouse'], address=args['address'])

        db.session.add(warehouse)
        db.session.commit()
        return warehouse, 201
    #####################################

    #función para listar los almacenes
    @service.doc(id='get-all-warehouses')
    @service.marshal_with(warehouse)
    def get(self):
        """lista todos los almacenes"""
        warehouses = db.session.query(Warehouse).all()
        return warehouses
####################################################################################
#Creamos una clase en la que vamos a poder listar, modificar y eliminar un almacén solo con su id:
@service.route('/<id>')
class WarehousesMethod(Resource):
    #Creamos una función para poder listar los detalles de un almacen de acuerdo a su ID
    @service.doc(id='get-warehouse-id')
    @service.marshal_with(warehouse)
    def get(self, id):
        """Lista de los detalles de un almacén de acuerdo a su ID"""
        warehouse = db.session.query(Warehouse).filter(Warehouse.id == id).first()
        #validamos que exista un almacen
        if not warehouse:
            abort(404, message=f'El almacén con el id:{id}, no existe')
        return warehouse
    ##################################################################
    
    #creamos una función para poder actualizar los datos de un almacen
    @service.doc(id='warehouse-update', parser=warehouse_args_update)
    @service.marshal_with(warehouse)
    def patch(self, id):
        """Actualiza los datos de un almacén"""
        #primero verificamos si existe el almacen:
        args = warehouse_args_update.parse_args()
        warehouse = db.session.query(Warehouse).filter(Warehouse.id == id).first()
        if not warehouse:
            abort(404, message=f'No existe ningún almacén con el ID: {id}')

        #podremos actualizar 1 o los 2 campos:
        #para ello, los validaremos que traigan datos.

        if args['warehouse']:
            warehouse.warehouse = args['warehouse']
        if args['address']:
            warehouse.address = args['warehouse']
        
        db.session.add(warehouse)
        db.session.commit()
        
        return warehouse, 201
    ################################################################
    
    @service.doc(id='delete-warehouse')
    def delete(self, id):
        """"Elimina un almacén"""
        warehouse_delete = db.session.query(Warehouse).filter(Warehouse.id == id).first()
        if not warehouse_delete:
            abort(404, message=f'el alamacén {id}, no existe')
        
        db.session.delete(warehouse_delete)
        db.session.commit()
        
        return {}, 204

    #################################################################

#creamos una clase para poder controlar el inventario en un almacén:
@service.route('/<id>/stock-warehouse')
class WarehouseStockListMethod(Resource):
    #función que enlista el stock de artìculos en un almacèn específico:
    @service.doc(id='get-stock-warehouse-list')
    @service.marshal_with(stock)
    def get(self, id):
        """Busca el stock de artìculos en un almacén específico"""
        stock = db.session.query(Stock).filter(Stock.warehouse_id == id).all()
        if not stock:
            abort(404, message=f'No hay stock de productos en la tienda con el id:{id}')
        return stock
    #################################################################

    #creamos una funciòn para poder registrar productos en un almacén:
    @service.doc(id='insert-stock-warehouse', parser=warehouse_args)
    @service.marshal_with(stock)
    def post(self, id):
        """Registra productos de un almacén"""
        args = warehouse_args.parse_args()
        product_in_stock = db.session.query(Stock).filter(
            Stock.warehouse_id==int(id), 
            Stock.item_sku==args['item_sku']
        ).first()
        if product_in_stock:
            abort(404, message=f'Este artículo ya se ha registrado en el almacen:{id}')
        stock = Stock(warehouse_id = int(id),
            item_sku = args['item_sku'],
            minimum_stock = args['minimum_stock'],
            stock = args['stock']
        )
        db.session.add(stock)
        db.session.commit()
        
        return stock, 201

    ################################################################
#creamos una clase para ajustar el stock de un almacén (se puede usar para descontar productos del inventario):
@service.route('/<id>/product-stock/<sku>')
class UpdateStockMethod(Resource):

    @service.doc(id='update-product-stock', parser=warehouse_args_update)
    @service.marshal_with(stock)
    def patch(self, id, sku):
        """actualiza el stock de un almacén, (se puede usar para descontar artículos)"""
        args = warehouse_args_update.parse_args()
        stock = db.session.query(Stock).filter(
            Stock.warehouse_id==int(id), 
            Stock.item_sku==int(sku)
        ).first()
        #validamos que aún haya stock en el almacén seleccionado
        if not stock:
            abort(404, message=f'***¡ADVERTENCIA!, ya no hay stock del producto {sku}')
        
        #Validamos que los campos del request no estén
        if args['minimum_stock'] != None:
            stock.minimum_stock = args['minimum_stock']

        if args['stock'] != None:
            stock.stock = args['stock']

        db.session.add(stock)
        db.session.commit()

        return stock, 201

####################################################################################
#podremos crear una api para realizar un reporte de los productos sin stock######
