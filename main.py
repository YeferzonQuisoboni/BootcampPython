#este archivo es un objeto, es decir un modulo, por lo tanto python le crea un atributo, que tiene por nombre __name__
from flask import Flask #estamos importando la calse Flask
from flask import session #Dict, para la sesión, para saber si el user esta uatenticado
from flask import request #para obtener los datos desde el form
from flask import redirect
from flask import render_template

from database import User
from database import Product

"""
Temas a consultar: 
    # BluePrint -> Organizar rutas
    # Migraciones -> Permite modificar las tablas sin perder la info
"""

#isntanciar, es decir crear un objeto de Flask y flask necesita un contexto de donde se ejecuta, por eso se le pasa la variable __name__
app = Flask(__name__)
app.secret_key = 'bootcamp_CodigoFacilito' #paea ofuscar la sesión

@app.route('/') #Decorar la función, esto para registrar una nueva ruta en el server,  para que la función decorada reposnda a dicha petición 
def index(): #primera vista para ello def una funcion
    #return 'Hola mundo!'
    return render_template('index.html')

"""
Mrthods:

GET -> Obtener un recurso
POST -> Crear un recurso
"""

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        print('el cliente envío un formulario:', request.form) #Dic
        #email = request.form['email']
        _email = request.form.get('email') #Se obtiene de froma segura por si no existe la llave
        _password = request.form.get('password')

        if _email and _password:
            user = User.create_user(_email, _password) #INSERT, cre el user en bd
            print(user.id)
            session['user'] = user.id #Se crea la sesión, ID del usuario en la bd
            return redirect('/products')

    return render_template('register.html') 

@app.route('/products')
def products():
    user = User.get(session['user'])
    #Obtener los prodcutos
    #products = Product.select().where(Product.user == user) #opción 1
    _products = user.products  #opción 2

    return render_template('products/index.html', products=_products) 


@app.route('/products/create', methods=['GET', 'POST'])
def products_create():

    if request.method == 'POST':
        _name = request.form.get('name') #Se obtiene de froma segura por si no existe la llave
        _price = request.form.get('price')

        if _name and _price:
            _user = User.get(session['user']) #Consulta la bd SELECT * from users WHERE id = <id>
            product = Product.create(name=_name, price=_price, user=_user) #INSERT INTO products(name, price, user_id) VALUES (name, price, user_id)
            return redirect('/products')

    return render_template('products/create.html') 

@app.route('/products/update/<id>', methods=['GET', 'POST'])
def products_update(id):
    ##_product = Product.get(id) Revisar
    _product = Product.select().where(Product.id == id).first()

    #Aqui irir el codigo para actualizar
    if request.method == 'POST':
        _product.name = request.form.get('name')
        _product.price = request.form.get('price')
        _product.save() #UPDATE products SET name='

        return redirect('/products')
 
    return render_template('products/update.html', product=_product)



@app.route('/products/delete/<id>', methods=['GET', 'POST'])
def products_delete(id):
    _product = Product.select().where(Product.id == id).first()

    if request.method == 'POST':
        product = Product.select().where(
            Product.id == id
        ).get()
        product.delete_instance()

        return redirect('/products')
 
    return render_template('products/delete.html', product=_product)


if __name__ == '__main__':
    app.run(debug=True)# para que el server se reinicie solo