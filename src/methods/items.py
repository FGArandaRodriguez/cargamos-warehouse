#Método de artículos, en esta clase se programan las funciones para la api de artículos.

#########################################################################################
#importamos las herramientas a utilizar:
#importamos los modelos:
from src.models.items import Item
#como tenemos una relación con la tabla stock, importamos su modelo: 
from src.models.stocks import Stock

#importamos flask: 
from flask_restplus import Marshal_with, fields, Resource, Namespace, abort
from database import db
########################################################################################

#creamos y le damos un nombre y una descripción al espacio de trabajo (se usará para la documentación):
service = Namespace('items', description='API para el control de los artículos')

################Creamos lo que en restfull serían los Schemas:######################################
#Documentamos los modelos a usar, les pondremos una nota como referencia a los campos
product = service.model('Product', {
    'sku': fields.Integer(required=False, description='Número de referencia'),
    'product': fields.String(required=True, description='Nombre del producto')
})
stock = service.model('Stock', {
    'id': fields.Integer(read_only=True, description='Número de referencia'),
    'store_id': fields.Integer(required=True, description='Número de referencia de la tienda'),
    'product_sku': fields.Integer(required=True, description='Número SKU del producto'),
    'minimum': fields.Integer(required=True, description='Existencia mínima'),
    'stock': fields.Integer(required=True, description='Existencia actual')
})

##################################################################################################


parser_item = service.parser()
parser_item.add_argument('sku', type=int, required=False, help='código/referencia del artículo')
parser_item.add_argument('item', type=str, required=True, help='Artículo')

update_product_parser = service.parser()
update_product_parser.add_argument('item', type=str, required=True, help='Nombre del artículo')




#########################################################################################

