#En este punto de inicio __init__ se harà la configuraciòn de las apis 
#desde aquì podremos configurar el inicio por default de las apis
#por lo que pondrémos la documentación de cada una de ellas

from flask_restplus import Api

# Importamos los Namespaces que creamos en cada metodo
from src.methods.items import service as items_namespace
from src.methods.warehouses import service as warehouses_namespace
from src.methods.stocks import service as stock_namespace


api_config = Api(
    title='Cargamos Warehouses', 
    description='Sistema de inventario de almacenes cargamos.'
)


api_config.add_namespace(items_namespace)
api_config.add_namespace(warehouses_namespace)
api_config.add_namespace(stock_namespace)