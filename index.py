from flask import Flask, render_template, request, redirect, url_for
from flask_assets import Bundle, Environment

app = Flask(__name__)

assets = Environment(app)
css = Bundle("src/main.css", output="dist/main.css")

assets.register("css", css)
css.build()

@app.route("/")
def index():
    # return "<h1>Hola mundo Erika</h1>"
    return render_template('index.html')

@app.route('/procesar_datos', methods=['POST'])
def procesar_datos():
    #AQUI RECUPERO LA INFORMACIÓN QUE SE MANDA DESDE EL FORMULARIO QUE SE ENCUENTRA EN EL index.html
    #AQUI VA EL CODIGO PARA PROCESAR LOS DATOS	 
    response = request.form
    array_data = []
    array_data = response['datos'].split(',')
    print(f"que imprime: {array_data}") #imprime el array (pueden mirarlo en la consola)
    return redirect(url_for('index')) #redirijo a la pagina index.html pierdan cuidado con esta linea de código

if __name__ == '__main__':
    app.run(debug=True, port=5000)