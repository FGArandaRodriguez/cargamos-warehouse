#En este archivo pondremos las pruebas unitarias de nuestros mètodos/funciones de api
#Para ello usaremos unit_test
from app import app
from database import db
import json
import unittest

class UnitTestApp(unittest.TestCase):

    #················Primero levantaremos los servicios···········#

    #creamos un mètodo para iniciar la applicación y la base de datos
    def UpServices(self):
        self.app = app.test_client()
        self.db = db.get_db()

    #······························································#

    ################### TEST Warehouse API: ########################
#Insertar un almacén:
    def test_create_warehouse(self):

        payload = json.dumps({
            "warehouse": "cargamos",
            "address": "conocida"
        })
        response = self.app.post(
            '/warehouses', 
            headers={"Content-Type": "application/json"}, 
            data=payload
        )
        self.assertEqual(201, response.status_code)
#Buscar un almacén
    def test_get_warehouse(self):
        response = self.app.get('/warehouses/3')
        self.assertEqual(200, response.status_code)

#Ver todas los almacenes:
    def test_get_warehouses(self):
        response = self.app.get('/warehouses')
        self.assertEqual(200, response.status_code)

#Actualizar un almacén:
    def test_update_warehouse(self):
        payload = json.dumps({
            "warehouse": "cargamos cancun"
        })
        response = self.app.patch(
            '/warehouses/1', 
            headers={"Content-Type": "application/json"}, 
            data=payload
        )
        self.assertEqual(201, response.status_code)
#Eliminar un almacén:
    def test_delete_warehouse_by_id(self):
        response = self.app.delete('/warehouses/3')
        self.assertEqual(204, response.status_code)

#···········Pruebas a artículos:
#creamos un artículo:
    def test_create_item(self):
        payload = json.dumps({
            "sku": 153910,
            "item": "carga pesada"
        })
        response = self.app.post(
            '/items', 
            headers={"Content-Type": "application/json"}, 
            data=payload
        )
        self.assertEqual(201, response.status_code)
#obtener un artículo por su sku:
    def test_get_item_by_sku(self):
        response = self.app.get('/items/153910')
        self.assertEqual(200, response.status_code)
#obtener todos los articulos:
    def test_get_all_items(self):
        response = self.app.get('/items')
        self.assertEqual(200, response.status_code)
#actualizar un articulo:
    def test_update_item(self):
        payload = json.dumps({
            "item": "carga liviana"
        })
        response = self.app.patch(
            '/items/153910', 
            headers={"Content-Type": "application/json"}, 
            data=payload
        )
        self.assertEqual(201, response.status_code)
#Eliminamos un articulo:
    def test_delete_item(self):
        response = self.app.delete('/items/153910')
        self.assertEqual(204, response.status_code)



###Test Stock:
    def test_create_stock(self):
        payload = json.dumps({
            "warehouse_id": 1,
            "item_sku": 153911,
            "minimum_stock": 10,
            "stock": 19
        })
        response = self.app.post(
            '/stock', 
            headers={"Content-Type": "application/json"}, 
            data=payload
        )
        self.assertEqual(201, response.status_code)
#update stock
    def test_update_stock_warehouse(self):
        payload = json.dumps({
            "stock": 8
        })
        response = self.app.post(
            '/warehouse/1/stock/153910', 
            headers={"Content-Type": "application/json"}, 
            data=payload
        )
        self.assertEqual(201, response.status_code)
    
