from cmath import sqrt
from operator import contains
from flask import Blueprint, Flask, render_template, request, redirect
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
    return render_template('index.html')

@app.route('/ayuda')
def ayuda():
    return render_template('help.html')

@app.route('/us')
def nosotros():
    return render_template('us.html')

@app.route('/procesar_datos', methods=['POST'])
def procesar_datos():
    #AQUI RECUPERO LA INFORMACIÓN QUE SE MANDA DESDE EL FORMULARIO QUE SE ENCUENTRA EN EL index.html
    #AQUI VA EL CODIGO PARA PROCESAR LOS DATOS	 
    response = request.form
    array_data, lista_Li_1, lista_Li, lista_Xi =  [],[],[],[]
    lista_ni, lista_fi, lista_Fi, lista_Ni, lista_densidad = [],[],[],[],[]
    #listas para los datos discretos
    lista_elem_dis, lista_frec_abs, lista_frec_rel, lista_Ni_dis, lista_Fi_dis = [],[],[],[], []
    diccionarioDatosContinuos, diccionarioDatosDiscretos = {}, {}
    
    array_data = response['datos'].split(',')
    
    float_array_data=[]
    for item in array_data:
        float_array_data.append(float(item))
        
    tipo_datos = response['tipo']
        
    #Ordenamos la lista 
    listaOrdenada = sorted(float_array_data)           

    if tipo_datos == "continuos":
            
        validacion = False
        for i in listaOrdenada:
            if(type(i) == float):
                validacion = True
                break
        #Se encuentra el mayor y menor valor que del array
        #valido cuanto le sumo 
        if validacion == True:            
            numMayor = mayor_de_arreglo(float_array_data) + 0.05
            numMenor = menor_de_arreglo(float_array_data) - 0.05
        else: 
            numMayor = mayor_de_arreglo(float_array_data) + 0.5
            numMenor = menor_de_arreglo(float_array_data) - 0.5
        #Cantidad de elementos ingresados
        n = len(float_array_data)
        print("n: ",n)
        rango = numMayor-numMenor
        m = round(1 + 3.3 * log(n,10))
        print("m: ",m)
        #Ancho de los intervalos
        c = round(rango/m, 2)
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
        lista_modas = moda_datos_continuos(diccionarioDatosContinuos, c, lista_ni)
        #print("moda: ", moda)
        varianza = varianza_datos_continuos(diccionarioDatosContinuos, n, media)
        #print("varianza: ",varianza)
        desviacionEstandar = math.sqrt(varianza)
        #print("desviacion estandar: ",desviacionEstandar)
        coef_variacion = (desviacionEstandar/media)*100
        #print("coeficiente de variacion: ",coef_variacion)
        length_list = len(lista_Li_1)
        validar_mas_modas = False
        if len(lista_modas) > 1: 
            validar_mas_modas = True
        lista_medidas_tendencia = [round(media, 3), round(mediana, 3),lista_modas]
        lista_indicadores_dispersion = [round(varianza, 3), round(desviacionEstandar, 3), round(coef_variacion, 3)]
        
        #lista para la la ojiva 
        lista_x_ojiva = []
        lista_x_ojiva.append(lista_Li_1[0])
        for i in lista_Li:
            lista_x_ojiva.append(i)
        lista_y_ojiva = []
        lista_y_ojiva.append(0)
        for i in lista_Fi:
            lista_y_ojiva.append(i*100)
        
        return render_template('result_continuous.html', lista_Li_1=lista_Li_1, lista_Li=lista_Li, 
                            lista_Xi=lista_Xi, lista_ni=lista_ni, lista_fi=lista_fi, 
                            lista_Ni=lista_Ni, lista_Fi=lista_Fi, lista_densidad=lista_densidad,
                            lista_medidas_tendencia=lista_medidas_tendencia, 
                            lista_indicadores_dispersion=lista_indicadores_dispersion,
                            c=c, length_list=length_list, validar_mas_modas=validar_mas_modas,
                            num_modas=len(lista_modas), lista_x_ojiva=lista_x_ojiva, lista_y_ojiva=lista_y_ojiva)
    
    else:
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
        media_dis = media_datos_discretos(listaOrdenada)
        mediana_dis = mediana_datos_discretos(listaOrdenada)
        varianza_dis = varianza_datos_discretos(listaOrdenada, media_dis)
        desviacionEstandar_dis = math.sqrt(varianza_dis)
        coef_variacion_dis = (desviacionEstandar_dis/media_dis)*100
        lista_modas_dis = []
        lista_modas_dis = moda_datos_discretos(lista_frec_abs, lista_elem_dis)
        length_list = len(lista_Li_1)
        validar_mas_modas = False
        if len(lista_modas_dis) > 1: 
            validar_mas_modas = True
        
        lista_medidas_tendencia = [round(media_dis, 3), round(mediana_dis, 3),lista_modas_dis]
        lista_indicadores_dispersion = [round(varianza_dis, 3), round(desviacionEstandar_dis, 3),
                                        round(coef_variacion_dis, 3)]
        #Saco el tamaño de la lista 
        length_list = len(lista_elem_dis)
    
    return render_template('result_discreet.html', lista_elem_dis=lista_elem_dis, lista_frec_abs=lista_frec_abs, 
                            lista_frec_rel=lista_frec_rel, lista_Ni_dis=lista_Ni_dis, lista_Fi_dis=lista_Fi_dis,
                            length_list=length_list, lista_modas_dis=lista_modas_dis, 
                            validar_mas_modas=validar_mas_modas, lista_medidas_tendencia=lista_medidas_tendencia,
                            lista_indicadores_dispersion=lista_indicadores_dispersion, num_modas=len(lista_modas_dis))

#FUNCIONES DE USO GENERAL
def mayor_de_arreglo(arreglo):
    """_summary_ = Devuelve el mayor elemento de un arreglo

    Args:
        arreglo (float, int, double): Arreglo de valores numericos

    Returns:
        float, int, double: El mayor elemento del arreglo
    """
    #El numero mayor se inicia suponiendo que el primer numero del arreglo es el mayor
    mayor = arreglo[0]
    #Recorrer y buscar
    for elemento in arreglo:
        if elemento > mayor:
            mayor = elemento
    return mayor

def menor_de_arreglo(arreglo):
    """_summary_ Devuelve el menor elemento de un arreglo

    Args:
        arreglo (int, float, double): Arreglo de valores numericos

    Returns:
        int, float, double: El menor elemento del arreglo
    """
    #El numero menor se inicia suponiendo que el primer numero del arreglo es el menor
    menor = arreglo[0]
    #Recorrer y buscar
    for elemento in arreglo:
        if elemento < menor:
            menor = elemento
    return menor

#FUNCIONES PARA DATOS CONTINUOS
def llenar_listas(lista_Li_1, lista_Li, lista_Xi, numMenor,c,m):
    """_summary_ Llena las listas de datos li-1, li, xi

    Args:
        lista_Li_1 (float): lista de datos li-1
        lista_Li (float): lista de datos li
        lista_Xi (float): lista de datos xi
        numMenor (float): numero menor de los datos
        c (float): ancho
        m (int): numero de intervalos
    """
    anterior = numMenor
    for i in range(m):        
        lista_Li_1.append(round(anterior, 3))
        siguiente = anterior+c
        lista_Li.append(round(siguiente, 3))
        Xi = (anterior+siguiente)/2
        lista_Xi.append(round(Xi, 3))
        anterior=siguiente
        
def  llenar_listas_frec(float_array_data, lista_Li_1, lista_Li, lista_ni, lista_fi, m, n):
    """_summary_ Llena las listas de datos ni y fi

    Args:
        float_array_data (float): arreglo de datos traidos desde la vista 
        lista_Li_1 (float): lista de datos li-1
        lista_Li (float): lista de datos li
        lista_ni (float): lista de datos ni a calcular
        lista_fi (float): lista de datos fi a calcular
        m (int): numero de intervalos
        n (int): numero de datos
    """
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
    """_summary_ Llena las listas de datos Ni

    Args:
        float_array_data (float): arreglo de datos traidos desde la vista 
        lista_ni (float): lista de datos ni
        lista_Ni (float): lista de datos ni a calcular
        m (int): numero de intervalos
    """
    lista_Ni.append(lista_ni[0])
    for i in range(m-1):
        niAnterior = lista_Ni[i]
        niSiguiente = lista_ni[i+1]
        nuevoValor = niAnterior + niSiguiente
        lista_Ni.append(round(nuevoValor, 3))
        
def llenar_lista_Fi(lista_fi, lista_Fi, m):
    """_summary_ Llena las listas de datos Fi

    Args:
        lista_fi (float): lista de datos fi
        lista_Fi (float): lista de datos fi a calcular
        m (int): numero de intervalos
    """
    lista_Fi.append(lista_fi[0])
    for i in range(m-1):
        niAnterior = lista_Fi[i]
        niSiguiente = lista_fi[i+1]
        nuevoValor = niAnterior + niSiguiente
        lista_Fi.append(round(nuevoValor, 3))

def llenar_lista_densidad(lista_fi, lista_densidad, m, c):
    """_summary_ Llena las listas de datos la función empirica de densidad

    Args:
        lista_fi (float): lista de datos fi
        lista_densidad (float): lista de datos la función empirica de densidad a calcular
        m (int): numero de intervalos
        c (float): ancho
    """
    for i in range(m):
        fid = (lista_fi[i]/c)*100
        lista_densidad.append(round(fid,3))
        
def media_datos_continuos(diccionarioDatContinuos, n):
    """_summary_ Calcula la media de los datos continuos

    Args:
        diccionarioDatContinuos (float): diccionario de datos continuos
        n (int): numero de datos

    Returns:
        float: media de los datos
    """
    media = 0
    for key in diccionarioDatContinuos:
        media += (diccionarioDatContinuos[key][2] * diccionarioDatContinuos[key][3])/n
    return media
   
def mediana_datos_continuos(diccionarioDatosContinuos, c):
    """_summary_ mediana de datos continuos

    Args:
        diccionarioDatosContinuos (_type_): diccionario de datos continuos
        c (float): ancho

    Returns:
        float: mediana de datos continuos
    """
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

def moda_datos_continuos(diccionarioDatosContinuos, c, lista_ni):
    """_summary_ moda de datos continuos

    Args:
        diccionarioDatosContinuos (float): diccionario de datos continuos
        c (float): ancho
        lista_ni (int): lista de los valores de la frecuencia absoluta (ni)

    Returns:
        float: Lista de modas de datos continuos
    """
    moda = 0
    lista_modas = []
    #saquemos el mayor de la lista del los ni 
    mayor_ni = mayor_de_arreglo(lista_ni)
    
    #verifico que no hayan mas de una moda 
    for i in range(0, len(lista_ni)): 
        if lista_ni[i] == mayor_ni:
            
            #calculo la moda 
            #primero saco el li-1 
            li_1 = diccionarioDatosContinuos[i+1][0]
            #calculo la moda
            moda = ((mayor_ni- lista_ni[i-1])/ ((mayor_ni - lista_ni[i-1]) + 
                    (mayor_ni - lista_ni[i+1]) )) * c + li_1
            lista_modas.append(round(moda, 3))
    
    return lista_modas

def varianza_datos_continuos(diccionarioDatosContinuos, n, media):
    """_summary_ varianza de datos continuos

    Args:
        diccionarioDatosContinuos (float): diccionario de datos continuos
        n (int): cantidad de datos
        media (float): media de los datos

    Returns:
        float: varianza de datos continuos
    """
    varianza = 0
    for key in diccionarioDatosContinuos:
        varianza += (((diccionarioDatosContinuos[key][2]-media)**2)*diccionarioDatosContinuos[key][3])/n
    return varianza    

#FUNCIONES PARA DATOS DISCRETOS
def frec_absolutas_discreta(listaOrdenada, lista_elem_dis, lista_frec_abs, lista_frec_rel):
    """_summary_ frecuencia absoluta de datos discretos

    Args:
        listaOrdenada (int): lista ordenada de datos discretos
        lista_elem_dis (_type_): lista de elementos discretos
        lista_frec_abs (_type_): lista de frecuencias absolutas
        lista_frec_rel (_type_): lista de frecuencias relativas
    """
    fi = 0
    n = len(listaOrdenada)
    cont = 1
    i = listaOrdenada[0]
    for j in range(len(listaOrdenada)):
        if (j<(len(listaOrdenada)-1)) and (listaOrdenada[j] == listaOrdenada[j+1]):
            cont += 1
        else:
            #Llenar la lista correspondiente a los valores de xi
            lista_elem_dis.append(int(listaOrdenada[j]))
            #Llenar la lista correspondiente a las frecuencias absolutas(ni)
            lista_frec_abs.append(cont)
            #Llenar la lista correspondiente a las frecuencias relativas(fi)
            fi = cont/n
            lista_frec_rel.append(round(fi, 3)) 
            cont =1

#Calculo de la media para datos discretos
def media_datos_discretos(lista):
    """_summary_ media de datos discretos

    Returns:
        float: media de datos discretos
    """
    media = sum(lista)/len(lista)
    return media
#Calculo de la mediana para datos discretos
def mediana_datos_discretos(lista):
    """_summary_ mediana de datos discretos

    Args:
        lista (int): lista de datos discretos

    Returns:
        float: mediana de datos discretos
    """
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
    """_summary_ varianza de datos discretos

    Args:
        lista (int): lista de datos discretos
        media (float): media de datos discretos

    Returns:
        float: varianza de datos discretos
    """
    tam = len(lista)
    varianza = 0
    for i in range(len(lista)):
        varianza += (((lista[i]-media)**2))/tam
    return varianza    
    
def moda_datos_discretos(lista_ni, lista_xi):
    """_summary_ moda de datos discretos

    Args:
        lista_ni (int): lista de los valores de la frecuencia absoluta (ni)
        lista_xi (int): lista de los datos xi

    Returns:
        float: Lista de modas de datos discretos
    """
    moda = 0
    lista_modas = []
    #saquemos el mayor de la lista del los ni 
    mayor_ni = mayor_de_arreglo(lista_ni)
    #verifico que no hayan mas de una moda 
    for i in range(0, len(lista_ni)): 
        if lista_ni[i] == mayor_ni:
            #calculo la moda 
            moda = lista_xi[i]
            lista_modas.append(moda)
    return lista_modas

if __name__ == '__main__':
    # app.run(debug=True, port=5000)
    app.run()