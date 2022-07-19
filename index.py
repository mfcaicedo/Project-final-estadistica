from cmath import sqrt
from flask import Flask, render_template, request, redirect, url_for
from flask_assets import Bundle, Environment
from math import log
import math

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
    array_data, lista_Li_1, lista_Li, lista_Xi =  [],[],[],[]
    lista_ni, lista_fi, lista_Fi, lista_Ni, lista_densidad = [],[],[],[],[]
    diccionarioDatosContinuos = {}
    
    array_data = response['datos'].split(',')
    print(f"que imprime: {array_data}") #imprime el array (pueden mirarlo en la consola)
    float_array_data=[]
    for item in array_data:
        float_array_data.append(float(item))
    
    #Se encuentra el mayor y menor valor que del array
    numMayor = mayor_de_arreglo(float_array_data)+0.05
    print("num mayor: ",numMayor)
    numMenor = menor_de_arreglo(float_array_data)-0.05
    print("num menor: ",numMenor)
    #Cantidad de elementos ingresados
    n = len(float_array_data)
    print("n: ",n)
    rango = numMayor-numMenor
    m = round(1 + 3.3 * log(n,10))
    print("m: ",m)
    #Ancho de los intervalos
    c = rango/m
    print("C:",c)
    
    #Llenar las listas correspondientes a los limites de los intervalos Li-1 y Li y a las marcas de clase (Xi)
    anterior = numMenor
    for i in range(m):        
        lista_Li_1.append(anterior)
        siguiente = anterior+c
        lista_Li.append(siguiente)
        Xi = (anterior+siguiente)/2
        lista_Xi.append(Xi)
        anterior=siguiente
    
    #Llenar la lista correspondiente a las frecuencias absolutas(ni)
    cont = 0
    fi = 0
    for j in range(m):
        for i in range(len(float_array_data)):
            if (float(float_array_data[i])>lista_Li_1[j]) and (float(float_array_data[i])<=lista_Li[j]):
                cont = cont+1
        lista_ni.append(cont)
        #Llenar la lista correspondiente a las frecuencias relativas(fi)   
        fi = cont/n
        lista_fi.append(fi)   
        cont = 0 
    
    #Llenar la lista correspondiente a las frecuencias absolutas acumuladas(Ni)
    lista_Ni.append(lista_ni[0])
    for i in range(m-1):
        niAnterior = lista_Ni[i]
        niSiguiente = lista_ni[i+1]
        nuevoValor = niAnterior + niSiguiente
        lista_Ni.append(nuevoValor)
        
    #Llenar la lista correspondiente a las frecuencias absolutas acumuladas(Ni)
    lista_Fi.append(lista_fi[0])
    for i in range(m-1):
        niAnterior = lista_Fi[i]
        niSiguiente = lista_fi[i+1]
        nuevoValor = niAnterior + niSiguiente
        lista_Fi.append(nuevoValor)
    
    #LLenar la lista correspondiente a la funcion empirica de densidad(fi*)
    for i in range(m):
        fid = (lista_fi[i]/c)*100
        lista_densidad.append(fid)
    
    #agregar a un diccionario 
    for i in range(m):
        list = [lista_Li_1[i], lista_Li[i], lista_Xi[i], lista_ni[i], lista_fi[i], lista_Ni[i], lista_Fi[i], lista_densidad[i]]
        diccionarioDatosContinuos[i+1] = list         
           
    #print(f"valores del diccionario: {diccionarioDatosContinuos}")       
    media = media_datos_continuos(diccionarioDatosContinuos, n)
    print("media: ",media)
    mediana = mediana_datos_continuos(diccionarioDatosContinuos, c) 
    print("mediana: ",mediana)
    moda = moda_datos_continuos(diccionarioDatosContinuos, c)
    print("moda: ", moda)
    varianza = varianza_datos_continuos(diccionarioDatosContinuos, n, media)
    print("varianza: ",varianza)
    desviacionEstandar = math.sqrt(varianza)
    print("desviacion estandar: ",desviacionEstandar)
    return redirect(url_for('index')) #redirijo a la pagina index.html pierdan cuidado con esta linea de código

def mayor_de_arreglo(arreglo):
    #El numero mayor se inicia suponiendo que el primer numero del arreglo es el mayor
    mayor = arreglo[0]
    #Recorrer y buscar
    for elemento in arreglo:
        if elemento > mayor:
            mayor = elemento
    return mayor

def menor_de_arreglo(arreglo):
    #El numero menor se inicia suponiendo que el primer numero del arreglo es el menor
    menor = arreglo[0]
    #Recorrer y buscar
    for elemento in arreglo:
        if elemento < menor:
            menor = elemento
    return menor

def media_datos_continuos(diccionarioDatContinuos, n):
    media = 0
    for key in diccionarioDatContinuos:
        media += (diccionarioDatContinuos[key][2] * diccionarioDatContinuos[key][3])/n
    return media
   
def mediana_datos_continuos(diccionarioDatosContinuos, c):
    mediana = 0
    indice = 0
    for key in diccionarioDatosContinuos:
        valor = 0.5
        if (diccionarioDatosContinuos[key][6]) < valor:
            indice += 1
            
    F_li_1 = diccionarioDatosContinuos[indice][6]
    fi = diccionarioDatosContinuos[indice+1][4]
    li_1 = diccionarioDatosContinuos[indice+1][0]
    
    mediana = (valor - F_li_1)*(c/fi) + li_1
    return mediana

def moda_datos_continuos(diccionarioDatosContinuos, c):
    moda =0
    #for key in diccionarioDatosContinuos:
        #ni = mayor_de_arreglo(diccionarioDatosContinuos[key],[3])
        #print("num mayor: ", ni)
    
    return moda

def varianza_datos_continuos(diccionarioDatosContinuos, n, media):
    varianza = 0
    for key in diccionarioDatosContinuos:
        varianza += (((diccionarioDatosContinuos[key][2]-media)**2)*diccionarioDatosContinuos[key][3])/n
    return varianza      

if __name__ == '__main__':
    app.run(debug=True, port=5000)