#En este archivo pondremos la configuración del desarrollo#
import os

#sacaremos la configuraciòn de la base de datos de las variables de entorno que creamos anteriormente.
db_params = {
    "user": os.environ['POSTGRES_USER'],
    "password": os.environ['POSTGRES_PASSWORD'],
    "host": os.environ['POSTGRES_HOST'],
    "port": os.environ['POSTGRES_PORT'],
    "database": os.environ['POSTGRES_DB'] 
}

class Config:
    SECRET_KEY = '7a7addffd392ef0a3a7c7fc349d93b87'
    PRESERVE_CONTEXT_ON_EXCEPTION = False
    SQLALCHEMY_DATABASE_URI = f'postgres://{db_params.get("user")}:{db_params.get("password")}@{db_params.get("host")}:{db_params.get("port")}/{db_params.get("database")}'
    SQLALCHEMY_TRACK_MODIFICATIONS = True