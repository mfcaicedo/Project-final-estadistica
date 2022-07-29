from cmath import sqrt
from flask import Blueprint, Flask, render_template, request, redirect, url_for
from flask_assets import Bundle, Environment
from math import log
import math
from collections import Counter

app = Flask(__name__)

assets = Environment(app)
css = Bundle("src/main.css", output="dist/main.css")

assets.register("css", css)
css.build()

# array_data = Blueprint('array_data', __name__)

@app.route("/")
def index():
    # return "<h1>Hola mundo Erika</h1>"
    return render_template('index.html')

@app.route('/result')
def busqueda():
    return render_template('result.html')


@app.route('/procesar_datos', methods=['POST'])
def procesar_datos():
    #AQUI RECUPERO LA INFORMACIÓN QUE SE MANDA DESDE EL FORMULARIO QUE SE ENCUENTRA EN EL index.html
    #AQUI VA EL CODIGO PARA PROCESAR LOS DATOS	 
    response = request.form
    print(f"response: {response}")
    array_data, lista_Li_1, lista_Li, lista_Xi =  [],[],[],[]
    lista_ni, lista_fi, lista_Fi, lista_Ni, lista_densidad = [],[],[],[],[]
    #listas para los datos discretos
    lista_elem_dis, lista_frec_abs, lista_frec_rel, lista_Ni_dis, lista_Fi_dis = [],[],[],[], []
    diccionarioDatosContinuos, diccionarioDatosDiscretos = {}, {}
    
    array_data = response['datos'].split(',')
    print(f"que imprime: {array_data}") #imprime el array (pueden mirarlo en la consola)
    
    float_array_data=[]
    for item in array_data:
        float_array_data.append(float(item))
        
    print(f"discreto {response['discreto']}")
    discretos = response['discreto']
    # constinuos = response['continuo']
        
    if discretos == "on":
        print("entro al if del discretos")
        
    listaOrdenada = sorted(float_array_data)           
    #Se encuentra el mayor y menor valor que del array
    numMayor = mayor_de_arreglo(float_array_data) + 0.05
    print("num mayor: ",numMayor)
    numMenor = menor_de_arreglo(float_array_data) - 0.05
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
    llenar_listas(lista_Li_1, lista_Li, lista_Xi, numMenor,c,m)
 
    #Llenar la lista correspondiente a las frecuencias absolutas(ni) y freccuencias relativas(fi)
    llenar_listas_frec(float_array_data, lista_Li_1, lista_Li, lista_ni, lista_fi, m, n)
       
    #Llenar la lista correspondiente a las frecuencias absolutas acumuladas(Ni)
    llenar_lista_Ni(lista_ni, lista_Ni, m)  
        
    #Llenar la lista correspondiente a las frecuencias relativas acumuladas(Fi)
    llenar_lista_Fi(lista_fi, lista_Fi, m)
        
    #LLenar la lista correspondiente a la funcion empirica de densidad(fi*)
    llenar_lista_densidad(lista_fi, lista_densidad, m, c)
    
    
    # return render_template('result.html',lista_Li_1=lista_Li_1, lista_Li=lista_Li, 
    #                         lista_Xi=lista_Xi, lista_ni=lista_ni, lista_fi=lista_fi, 
    #                         lista_Fi=lista_Fi, lista_Ni=lista_Ni, lista_densidad=lista_densidad, c=c)
    
    
    #agregar a un diccionario 
    for i in range(m):
        list = [lista_Li_1[i], lista_Li[i], lista_Xi[i], lista_ni[i], lista_fi[i],
                lista_Ni[i], lista_Fi[i], lista_densidad[i]]
        
        diccionarioDatosContinuos[i+1] = list    
        
        
        
             
     
    #VALORES CONTINUOS   
    media = media_datos_continuos(diccionarioDatosContinuos, n)
    #print("media: ",media)
    mediana = mediana_datos_continuos(diccionarioDatosContinuos, c) 
    #print("mediana: ",mediana)
    moda = moda_datos_continuos(diccionarioDatosContinuos, c)
    #print("moda: ", moda)
    varianza = varianza_datos_continuos(diccionarioDatosContinuos, n, media)
    #print("varianza: ",varianza)
    desviacionEstandar = math.sqrt(varianza)
    #print("desviacion estandar: ",desviacionEstandar)
    coef_variacion = (desviacionEstandar/media)*100
    #print("coeficiente de variacion: ",coef_variacion)
    
    #VALORES DISCRETOS    
    frec_absolutas_discreta(listaOrdenada, lista_elem_dis, lista_frec_abs, lista_frec_rel)
    
    #Llenar la lista correspondiente a las frecuencias absolutas acumuladas(Ni)
    llenar_lista_Ni(lista_frec_abs, lista_Ni_dis, len(lista_elem_dis))    
    #Llenar la lista correspondiente a las frecuencias relativas acumuladas(Fi)
    llenar_lista_Fi(lista_frec_rel, lista_Fi_dis, len(lista_elem_dis))
    #Agregar a un diccionario
    for i in range(len(lista_elem_dis)):
        list = [lista_elem_dis[i], lista_frec_abs[i], lista_frec_rel[i], lista_Ni_dis[i], lista_Fi_dis[i]]
        diccionarioDatosDiscretos[i+1] = list 
    print(f"lista elementos: {listaOrdenada}")    
    media_dis = media_datos_discretos(listaOrdenada)
    print("media: ",media_dis)
    print(f"lista ordenada: {listaOrdenada}")
    mediana_dis = mediana_datos_discretos(listaOrdenada)
    print("mediana: ",mediana_dis)
    varianza_dis = varianza_datos_discretos(listaOrdenada, media_dis)
    print("varianza: ",varianza_dis)
    desviacionEstandar_dis = math.sqrt(varianza_dis)
    print("desviacion estandar: ",desviacionEstandar_dis)
    coef_variacion_dis = (desviacionEstandar_dis/media_dis)*100
    print("coeficiente de variacion: ",coef_variacion_dis)
    moda_datos_discretos(listaOrdenada)
    print("lista elementos: ",lista_Li_1)
    print("diccionarioDatosContinuos: ",diccionarioDatosContinuos) 
    length_list = len(lista_Li_1)
    c = round(c,4)
    
    # return render_template('result.html', diccionarioDatosDiscretos=diccionarioDatosDiscretos, 
    #                     c=c, length_list=length_list,)
    return render_template('result.html', lista_Li_1=lista_Li_1, lista_Li=lista_Li, 
                            lista_Xi=lista_Xi, lista_ni=lista_ni, lista_fi=lista_fi, 
                            lista_Ni=lista_Ni, lista_Fi=lista_Fi, lista_densidad=lista_densidad,
                            c=c, length_list=length_list)
    # return redirect(url_for('index')) #redirijo a la pagina index.html pierdan cuidado con esta linea de código

#FUNCIONES DE USO GENERAL
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

#FUNCIONES PARA DATOS CONTINUOS
def llenar_listas(lista_Li_1, lista_Li, lista_Xi, numMenor,c,m):
    anterior = numMenor
    for i in range(m):        
        lista_Li_1.append(anterior)
        siguiente = anterior+c
        lista_Li.append(siguiente)
        Xi = (anterior+siguiente)/2
        lista_Xi.append(Xi)
        anterior=siguiente
        
def  llenar_listas_frec(float_array_data, lista_Li_1, lista_Li, lista_ni, lista_fi, m, n):
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
def llenar_lista_Ni(lista_ni, lista_Ni, m):
    lista_Ni.append(lista_ni[0])
    for i in range(m-1):
        niAnterior = lista_Ni[i]
        niSiguiente = lista_ni[i+1]
        nuevoValor = niAnterior + niSiguiente
        lista_Ni.append(nuevoValor)
        
def llenar_lista_Fi(lista_fi, lista_Fi, m):
    lista_Fi.append(lista_fi[0])
    for i in range(m-1):
        niAnterior = lista_Fi[i]
        niSiguiente = lista_fi[i+1]
        nuevoValor = niAnterior + niSiguiente
        lista_Fi.append(nuevoValor)

def llenar_lista_densidad(lista_fi, lista_densidad, m, c):
    for i in range(m):
        fid = (lista_fi[i]/c)*100
        lista_densidad.append(fid)
        
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

#FUNCIONES PARA DATOS DISCRETOS
def frec_absolutas_discreta(listaOrdenada, lista_elem_dis, lista_frec_abs, lista_frec_rel):
    fi = 0
    n = len(listaOrdenada)
    cont = 1
    #[1 1 2 2 3 3 4 4]
    i = listaOrdenada[0]
    for j in range(len(listaOrdenada)):
        if (j<(len(listaOrdenada)-1)) and (listaOrdenada[j] == listaOrdenada[j+1]):
            cont += 1
        else:
            #Llenar la lista correspondiente a los valores de xi
            lista_elem_dis.append(listaOrdenada[j])
            #Llenar la lista correspondiente a las frecuencias absolutas(ni)
            lista_frec_abs.append(cont)
            #Llenar la lista correspondiente a las frecuencias relativas(fi)
            fi = cont/n
            lista_frec_rel.append(fi) 
            cont =1

#Calculo de la media para datos discretos
def media_datos_discretos(lista):
    media = sum(lista)/len(lista)
    return media
#Calculo de la mediana para datos discretos
def mediana_datos_discretos(lista):
    tam = len(lista)
    if(tam % 2 == 0):
        mitad = tam/2
        mitad = int(mitad)
        print("mitad: ", mitad)
        mediana = (lista[mitad - 1] + lista[mitad])/2
        print("midiana: ", mediana)
    else:
        mitad = (tam // 2)+1
        mediana = lista[mitad]
    return mediana
    
def varianza_datos_discretos(lista, media):
    tam = len(lista)
    varianza = 0
    for i in range(len(lista)):
        varianza += (((lista[i]-media)**2))/tam
    return varianza    
     
def moda_datos_discretos(lista):
    counter = Counter(lista)
    primero,segundo, *_,last = counter.most_common()
    print(primero, segundo)
    

if __name__ == '__main__':
    app.run(debug=True, port=5000)