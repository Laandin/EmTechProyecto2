# -*- coding: utf-8 -*-
"""
Created on Wed Oct  6 21:01:20 2021

@author: Luis ML
"""

import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
%matplotlib inline


#Se definen las funciones que se ocuparán en el análisis de datos 

#Definimos una función que al ingresar una lista y la posición del valor seleccionado, esta nos la ordenará 
def ordena(lista,n):
    numero = len(lista)
    i= 0
    while (i < numero):
        j = i
        while (j < numero):
            if(lista[i][n] > lista[j][n]):
                temp = lista[i]
                lista[i] = lista[j]
                lista[j] = temp
            j= j+1
        i=i+1
    return lista 


#Definimos una función que nos va a regresar una base
#n = El número de la opción que vamos a usar(1,2,3)
#comp = La columna por la cual vamos a segmentar los datos
#La función comprueba la opción elegida y nos regresa una base y el nombre de las columnas 
def opciones(n, comp):
    if n == 1:
        opc = list(zip(datitos['direction'],datitos['origin'],datitos['destination'],datitos[comp]))
        cname = ['origin','destination', comp, 'uso_ruta','total_value' ]
    elif n ==2:
        opc = list(zip(datitos['direction'],datitos['transport_mode'],datitos[comp]))
        cname = ['transport_mode', comp, 'uso_ruta','total_value' ]
    elif n ==3:
        opc = list(zip(datitos['direction'],datitos['origin'],datitos[comp]))
        cname = ['origin', comp, 'uso_ruta','total_value' ]
    return opc, cname
          

#Esta función nos dará la base ya segmentada con el uso de lo que solicitemos 
#paises =  Es la base que vamos a segmentar 
#comp = La columna por la cual vamos a segmentar los datos 
#cname = vector con el nombre de las columnas 
#filtro = si queremos hacer un filtro en nuestra base 
def datos_por_segmentacion(paises,comp, cname, filtro = 0):
    
    #Definimos dos listas
    #La primera nos pega la base pedida y el valor que generó estás
    #La segunda quitamos los valores duplicados 
    valor = list(zip(paises,datitos['total_value']))
    rut = list(set(paises))
    
    #Generamos una nueva lista para contar el uso y el valor que genera lo solicitado
    rutas=[]
    for i in rut:
        agreg = [i,0,0]
        rutas.append(agreg)
        
    #Encontramos las veces y el valor de las rutas o la segmentación seleccionada 
    for i in valor:
        for j in rutas:
            if i[0] == j[0]:
                j[1] = j[1] + 1
                j[2] = j[2] + i[1]
    
    #Obtenemos los valores segmentados por exportaciones e importaciones              
    rutas = list(reversed(ordena(rutas,1)))
    imp = []
    exp = []
    
    for i in rutas:
        if i[0][0] == 'Exports':
            agreg = []
            for m  in range(len(i[0])-1):
                agreg.append(i[0][m+1])
            agreg.append(i[1])
            agreg.append(i[2])
            exp.append(agreg)
        elif i[0][0] == 'Imports':
            agreg = []
            for m  in range(len(i[0])-1):
                agreg.append(i[0][m+1])
            agreg.append(i[1])
            agreg.append(i[2])
            imp.append(agreg) 
            
    
    
    imp = pd.DataFrame(imp)
    exp = pd.DataFrame(exp)
    imp.columns = cname
    exp.columns = cname
    
    if filtro != 0:
        imp = imp[imp[comp] == filtro]
        exp = exp[exp[comp] == filtro]
    
    return imp, exp


#Definimos una función para graficar nuestros datos 
#base = la base para obtener los dtaos a graficar 
#Años = los años que vamos a revisar
#r = Si es Importación o Exportación
def graf(base, años, r):
    
    plt.barh(base['origin'].head(10)+" - "+base['destination'].head(10),base['uso_ruta'].head(10))
    plt.ylabel('País')
    plt.xlabel('Uso de ruta')
    plt.title(r)
    plt.show()
    
    for i in años:
        base0 = base[base['year'] == i]
        base0.reset_index(inplace = True, drop = True)
        plt.barh(base0['origin'].head(10)+" - "+base0['destination'].head(10),base0['uso_ruta'].head(10))
        plt.ylabel('País')
        plt.xlabel('Uso de ruta')
        plt.title(r + " en el año " + str(i))
        plt.show()
    
#Esta función la ocupamos para agrupar los datos
#base = la base solicitada
#años = los años que vamos a revisar
#x, y las columnas a elegir 
def obt(base, años,x,y):
    mode = list(set(base[x]))
    listita = list(zip(base[x],base[y]))
    
    modo = []
    for i in mode:
        agreg = [i,0]
        modo.append(agreg)
    
        
    for i in listita:
        for j in modo:
            if i[0] == j[0]:
                j[1] += i[1]
    return modo


#Graficamos a partir de una base 
def grafi(modo,r,x,y,z):               
    modo = pd.DataFrame(modo) 
    modo.columns = [x,y]           
    plt.barh(modo[x],modo[y])
    plt.ylabel(z)
    plt.xlabel('Valor')
    plt.title(r)
    plt.show()

#Definimos esta función para obetenr la muestra de unos datos
#percent = el % de datos que queremos 
def muestra(base,percent):
    base = list(reversed(ordena(base,1)))
    total = 0
    
    for i in base:
        total = total + i[1]
       
    lim = total*percent
    muest = []
    acum = 0
    
    for i in base:
        acum += i[1]
        if acum <= lim:
            muest.append(i)
    
    return muest
    


"------------------------------------------------ R E S U L T A D O S ------------------------------------------------"
#leemos el csv de la base y lo guardamos en una variable
datitos = pd.read_csv("C:/Users/Luis ML/Desktop/data-science-proyecto2-master/synergy_logistics_database.csv")
años = list(set(datitos['year']))
años.sort()


#Opción 1
n = 1
comp = 'year'

#Obtemos loas bases a partir de las funciones difinidas 
basse, name = opciones(n, comp)
imp, exp = datos_por_segmentacion(basse, comp,name)

#10 más demandadas
#importaciones 
imp.head(10)
#exportaciones
exp.head(10)

#Graficamos las importaciones y exportaciones global y por año         
graf(imp, años, 'Importaciones')
graf(exp, años, 'Exportaciones')
    
        


#Opción 2 
m = 2
comp = 'year'
x= "transport_mode"
y='total_value'
z='Medio de transporte'


#Obtemos loas bases a partir de las funciones difinidas 
basse, name = opciones(m, comp)
imp2, exp2 = datos_por_segmentacion(basse, comp,name)

#Graficamos 
grafi(obt(imp2, años,x,y), 'Importaciones', x, y,z)
grafi(obt(exp2, años,x,y), 'Exportaciones', x, y,z)




#Opción 3
n = 3
comp = 'year'
b= "origin"
c='País'
percent = .8


#Obtemos loas bases a partir de las funciones difinidas 
basse, name = opciones(n, comp)
imp3, exp3 = datos_por_segmentacion(basse, comp,name)

#Agrupamos los datos por país
paisi = obt(imp3, años, b, y)
paise = obt(exp3,años, b,y)

#Obtenemos la muestra 
mu = muestra(paisi, percent)
mu1 = muestra(paise, percent)

#Graficamos 
grafi(mu, 'Importaciones', b,y,c)
grafi(mu1,'Exportaciones',b,y,c)



















