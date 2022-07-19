from ast import If


mensaje = "hola a todos"
print(mensaje)

diasSemana = ['lunes', 'martes', 'miercoles', 'jueves', 'viernes']

if(diasSemana):
    print(diasSemana[1])
    
    
prueba = {
    1: [1.5, 2.5, 2, 5, 8],
    2: [2.5, 7.5, 2, 4, 7],
    3: [7.5, 8.5, 5, 3, 9],
}

# print(prueba)

for key in prueba:
    # print(key)
    if key == 2: # el que
        print(f" esta es la ultima posicion {prueba[key][4]}")
    # print('\n')
    
    

print("PEDIR DATOS POR CONSOLA")
lista_valores = []
diccionario = {}
while(True):
    valor = float(input("Digite el valor: "))
    lista_valores.append(valor)
    bandera = input("Desea continuar? (s/n): ")
    if bandera.lower() == 'n':
        break
    

#agregar a un diccionario 
for i in range(len(lista_valores)):
    list = [lista_valores[i], lista_l2[i], lista_l3[i]]
    diccionario[i+1] = list  

print("valoes digitaodos: ")
for i in lista_valores:
    print(i)

print(f"valores del diccionario: {diccionario}")

"""
print("valores digitaodos Ni: ")
    for j in lista_Ni:
      print(j)   
      
    print("valores digitaodos Fi: ")
    for j in lista_Fi:
      print(j)  
        
    print("valores digitaodos fi: ")
    for j in lista_fi:
       print(j)
       
    print("valores digitaodos ni: ")
    for j in lista_ni:
        print(j)
     
    print("valores digitaodos li-1: ")
    for j in lista_Li_1:
        print(j)

    print("valores digitaodos li: ")
    for j in lista_Li:
        print(j)
    
    print("valores digitaodos Xi: ")
    for j in lista_Xi:
       print(j)  
       
    print("valores densidad fi*: ")
    for j in lista_densidad:
       print(j) 
"""  