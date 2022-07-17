diccionario = {
    "nombre" : "Juan", 
    "edad" : 18,
    "celular" : 3235394
}
llaves = diccionario.keys()
ll = diccionario.items()
print(ll)

print(f"{llaves}")

# for key in diccionario: 
#     print(f"key : {key} : valor: {diccionario[key]} ")


dicc2 = {
    "nombres" : ["milton", "ferney", "juan"],  
    2: "valor2"
}

for key in dicc2: 
    print(f"{dicc2[key][0]}")
    

lista = [1,3,4,3]
print(lista[0])


dic = {}

for i in range(0, len(lista)): 
    ii = str(i)
    dic[ii] = lista[i]

# print(dic)

for i in dic: 
    print(f"{dic[i]}")
    print(f"{type(i)}")

    
    