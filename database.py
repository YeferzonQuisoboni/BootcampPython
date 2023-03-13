from peewee import *
from decouple import config

import datetime

db = MySQLDatabase(
    'tienda',
    user='root',
    password='',
    #password = config('password'),
    port=3306,
    host='localhost'
)

#Trabajando con el ORM


class User(Model): #tabla User
    email = TextField()
    password = TextField()
    created_at = DateTimeField() ##default=datetime.datetime.now

    class Meta: #Utilizar la clase Meta para definir la bd a la cual nos vamos a conectar 
        database = db # base de datso
        db_table = 'users' # Definir el nombre de la tabla, por defecto peewee toma el nombre de la clase, pero no es recomendable, ya eque esta en siingular

    @classmethod
    def create_user(cls,_email, _password):
        #Validar que el correo sea único
           #codigo de la validación
        _password = 'cody_' + _password #Algoritmo de encrypt solo es un ejemplo
        return User.create(email=_email, password=_password)


class Product(Model):
    name = TextField()
    price = IntegerField()
    user = ForeignKeyField(User, backref='products')
    created_at = DateTimeField(default=datetime.datetime.now)

    #Properties
    @property
    def price_format(self):
        return f"${self.price // 100} dólares"


    class Meta: 
        database = db 
        db_table = 'products'


#Crear la tabla
db.create_tables( [User, Product] )