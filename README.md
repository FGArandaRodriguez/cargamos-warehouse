# cargamos-warehouse
Proyecto para llevar el control de un stock de productos en uno o varios almacenes, realizado con FLASK RESTPLUS y PostgreSQL

## Requerimientos
### 1.- Para correr el proyecto, es necesario tener instalado lo siguiente: 

- Python3
- docker (docker-engine)
- docker-compose

A pesar de que usaremos una base de datos PostgreSQL, la instalación de este gestor no será necesaria, ya que usaremos Docker

## Ejecución del proyecto:

Para ejecutar el proyecto, es necesario: 

- Clonar el proyecto:
```sh
$ git clone git@github.com:FGArandaRodriguez/cargamos-warehouse.git
```
- Crearemos las imagen docker:
```sh
$ docker-compose -f docker-compose.yml build
```
- Corremos el contenedor, para correr el proyecto:
```sh
$ docker-compose -f docker-compose.yml up
```

El contenedor correrá en el puerto 5000, por lo que podemos ir al navegador y entrar a la dirección:
```
localhost:5000
```
El proyecto tiene configurado iniciar por defecto con la documentación generada por Swagger 

- Swagger es un conjunto de herramientas de software de código abierto para diseñar, construir, documentar, y utilizar servicios web RESTful. Fue desarrollado por SmartBear Software e incluye documentación automatizada, generación de código, y generación de casos de prueba.

Esto nos permitirá que, en el mismo navegador podramos ver lo siguiente:

- ver el menú de apis disponibles en este proyecto, 
- realizar pruebas desde el mismo navegador,
- ver la documentación de cada api

### Referencias: 

En este apartado, dejaré algunas referencias que me fueron útiles para realizar este proyecto:

- Instalacin de Docker engine y Docker compose desde linux
  -https://docs.docker.com/compose/install/

  -https://docs.docker.com/engine/install/ubuntu/

- Python Argparser()
  - https://docs.python.org/3/library/argparse.html

- Pruebas con unit-test
  -https://rico-schmidt.name/pymotw-3/unittest/
  
- fundamentos de python, estructura de un proyecto restplus
  - https://platzi.com/tutoriales/1104-python/4672-fundamentos-de-python-modulos-paquetes-y-namespace/
  - https://levelup.gitconnected.com/dockerizing-a-flask-application-with-a-postgres-database-b5e5bfc24848

- Diferencias entre PUT y PATCH:
  -https://medium.com/backticks-tildes/restful-api-design-put-vs-patch-4a061aa3ed0b
  
- Documentación y uso de Swagger
  -https://flask-restplus.readthedocs.io/en/stable/swagger.html
  -https://www.genbeta.com/desarrollo/swagger-framework-para-generar-documentacion-de-apis-restful-y-un-sandbox-para-probar-llamadas



