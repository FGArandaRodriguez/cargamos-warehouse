#Método de artículos, en esta clase se programan las funciones para la api de artículos.

#########################################################################################
#importamos las herramientas a utilizar:
#importamos los modelos:
from src.models.items import Item
#como tenemos una relación con la tabla stock, importamos su modelo: 
from src.models.stocks import Stock

#importamos flask: 
from flask_restplus import marshal_with, fields, Resource, Namespace, abort
from database import db
########################################################################################

#creamos y le damos un nombre y una descripción al espacio de trabajo (se usará para la documentación):
service = Namespace('items', description='API para el control de los artículos')

################Creamos lo que en restfull serían los Schemas:######################################
#Documentamos los modelos a usar, les pondremos una nota como referencia a los campos
item = service.model('Item', {
    'sku': fields.Integer(required=False, description='Identificador/referencia de un artículo'),
    'item': fields.String(required=True, description='Nombre del artículo')
})
stock = service.model('Stock', {
    'id': fields.Integer(read_only=True, description='Identificador'),
    'warehouse_id': fields.Integer(required=True, description='Identificador del almacen'),
    'item_sku': fields.Integer(required=True, description='SKU del artìculo'),
    'minimum_stock': fields.Integer(required=True, description='Stock minimo'),
    'stock': fields.Integer(required=True, description='Stock real')
})

##################################################################################################
#####definimos los argumentos que usaremos #####
item_args = service.parser()
item_args.add_argument('sku', type=int, required=False, help='código/referencia del artículo')
item_args.add_argument('item', type=str, required=True, help='Artículo')

items_update_args= service.parser()
items_update_args.add_argument('item', type=str, required=True, help='Nombre del artículo')
#########################################################################################


#usaremos el decorador @route para asignarle una ruta, como usamos restplus
#podrèmos usar una misma ruta con diferentes verbos http

@service.route('/')
class ItemsMethod(Resource):
    #usaremos el decorador .doc para asignarle un identificador a la funciòn
    @service.doc(id='item-post', parser = item_args)
    #usaremos el marshall with para realizar un "dump"/ crear un objeto serializado 
    #de acuerdo al schema
    @service.marshal_with(item)
    #creamos una funciòn para insertar artículos:
    def post(self):
        """Agrega artículos"""
        args = item_args.parse_args()
        #asignamos el valor al campo item, al ser requerido, el modelo validará por nosotros 
        #que el campo estè lleno
        item = Item(item=args['item'])
        
        #validamos que no se puedan asignar los mismos skus ya registrados a otros articulos
        #validamos que se nos haya pasado el parametro sku
        if args['sku']:
            if db.session.query(Item).filter(Item.sku==args['sku']):
                item.sku = args['sku']
            else:
                abort(404, message=f'El item con el SKU:{args["sku"]} , ya existe, por favor, asigne otro SKU')
        
        db.session.add(item)
        db.session.commit()
        
        return item, 201
    #################################################################################################3####
    
    #creamos una funcion para listar artìculos disponibles con la misma estructura que la anterior
    @service.marshal_with(item)
    @service.doc(id='items-get')
    def get(self):
        """Lista de artículos disponibles"""
        items = db.session.query(Item).all()
        return items
    
######################################################################################################
#crearemos otra clase con la misma estructura, pero esta vez para poder editar y eliminar artìculos.
@service.route('/<sku>')
class ItemMethod(Resource):

    @service.doc(id='item-update', parser=items_update_args)
    @service.marshal_with(item)
    #(usamos patch ya que solo actuallizaremos el nombre del artìculo)
    def patch(self, sku):
        """Edita un artìculo"""
        args = items_update_args.parse_args()
        #buscaremos el item por su sku
        item = db.session.query(Item).filter(Item.sku == sku).first()
        if not item:
            abort(404, message=f'El artículo con el SKU: {sku}, no existe, por favor registrelo.')
        item.item = args['item']
        
        db.session.add(item)
        db.session.commit()
        return item, 201
    ################################################################
    #creamos una funcion para eliminar

    @service.doc(id='item-delete')
    def delete(self, sku):
        """Elimina un artículo"""
        item_delete = db.session.query(Item).filter(Item.sku == sku).first()
        if not item_delete:
            abort(404, message=f'El artículo {sku} no existe')
        
        db.session.delete(item_delete)
        db.session.commit()
        
        return {}, 204
    
    @service.doc(id='item-get-by-sku')
    @service.marshal_with(item)
    def get(self, sku):
        """busca un artìculo de acuerdo a su sku"""
        item_get = db.session.query(Item).filter(Item.sku == sku).first()
        if not item_get:
            abort(404, message=f'No se encontró algún artículo con el sku:{sku}')
        return item_get




    
    
