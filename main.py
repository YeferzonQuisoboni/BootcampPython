#este archivo es un objeto, es decir un modulo, por lo tanto python le crea un atributo, que tiene por nombre __name__
from flask import Flask #estamos importando la calse Flask
from flask import render_template

#isntanciar, es decir crear un objeto de Flask y flask necesita un contexto de donde se ejecuta, por eso se le pasa la variable __name__
app = Flask(__name__)

@app.route('/') #Decorar la función, esto para registrar una nueva ruta en el server,  para que la función decorada reposnda a dicha petición 
def index(): #primera vista para ello def una funcion
    #return 'Hola mundo!'
    return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True)# para que el server se reinicie solo