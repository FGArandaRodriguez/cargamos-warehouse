###Archivo con las configuraciones de la aplicación_:###
from flask import Flask
from config import Config
from database import db
#importamos laconfiguracion de nuestras apis
from src import api_config

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)
api_config.init_app(app)

with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')