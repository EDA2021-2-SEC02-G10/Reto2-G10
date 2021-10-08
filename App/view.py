"""
 * Copyright 2020, Departamento de sistemas y Computación, Universidad
 * de Los Andes
 *
 *
 * Desarrolado para el curso ISIS1225 - Estructuras de Datos y Algoritmos
 *
 *
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along withthis program.  If not, see <http://www.gnu.org/licenses/>.
 """

import config as cf
import controller
from DISClib.ADT import list as lt
from DISClib.ADT import map as mp
from DISClib.DataStructures import mapentry as me
assert cf
import sys
default_limit = 1000
sys.setrecursionlimit(default_limit*10)

"""
La vista se encarga de la interacción con el usuario
Presenta el menu de opciones y por cada seleccion
se hace la solicitud al controlador para ejecutar la
operación solicitada
"""


def printSortedResults(result):

    print('En el rango dado hay: ' + str(result[1]))
    print('De esas obras se compraron: '+ str(result[2]))
    print('Las primeras 3 obras del rango en base a su fecha de creacion son: ')
    print(result[0]['elements'][0])
    print(result[0]['elements'][1])
    print(result[0]['elements'][2])
    print('Las ultimas 3 obras del rango en base a su fecha de creacion son: ')
    print(result[0]['elements'][-1])
    print(result[0]['elements'][-2])
    print(result[0]['elements'][-3])


def printArtworksbyNationality(result):

    final_list = lt.subList(result[0], 1, 10)

    firstDatalst = [result[1]['elements'][0], result[1]['elements'][1], result[1]['elements'][2], result[1]['elements'][3], result[1]['elements'][4]]
    lastDatalst = [result[1]['elements'][-1], result[1]['elements'][-2], result[1]['elements'][-3], result[1]['elements'][-4], result[1]['elements'][-5]]

    print('En base al numero de obras en el MoMA por pais, ')
    print('Los TOP 10 paises en el MoMA son : ')
    print(final_list['elements'])
    size = lt.size(result[1])
    print('El numero de obras en la lista de obras del pais TOP 1 es: ' + str(size))
    print('Las primeras 3 obras de la lista del pais TOP 1 son: ')
    print(firstDatalst[0])
    print(firstDatalst[1])
    print(firstDatalst[2])
    print('Las ultimas 3 obras de la lista del pais TOP 1 son: ')
    print(lastDatalst[0])
    print(lastDatalst[1])
    print(lastDatalst[2])


def printMoveDepartment(result):

    print('El valor aproximado de mover todas las obras del departamento es: ' + str(result[0]))
    print('El peso aproximado de todas las obras del departamento es: ' + str(result[1]))
    print('Las 5 obras mas antiguas del departamento a mover son: ')
    print(result[2]['elements'][0])
    print(result[2]['elements'][1])
    print(result[2]['elements'][2])
    print(result[2]['elements'][3])
    print(result[2]['elements'][4])
    print('Las 5 obras mas costosas de mover son: ')
    print(result[3]['elements'][-1])
    print(result[3]['elements'][-2])
    print(result[3]['elements'][-3])
    print(result[3]['elements'][-4])
    print(result[3]['elements'][-5])


def printMenu():
    print("Bienvenido")
    print("1- Cargar información en el catálogo")
    print("2- Listar cronologicamente los artistas")
    print("3- Listar cronologicamente las adquisiciones")
    print("4- Clasificar las obras de un artista por técnica")
    print("5- Clasificar las obras por la nacionalidad de sus creadores")
    print("6- Transportar obras de un departamento")
    print("7- Encontrar los artistas mas prolificos del museo")
    print("0- Salir de la aplicacion")


catalog = None

"""
Menu principal
"""
while True:
    printMenu()
    inputs = input('Seleccione una opción para continuar\n')
    if int(inputs[0]) == 1:
        print("Cargando información de los archivos ....")
        catalog = controller.initCatalog()
        controller.loadData(catalog)
        sizeArtworks = lt.size(catalog['artworks'])
        print('Obras cargadas: ' + str(sizeArtworks))
        listArtistsloaded = mp.keySet(catalog['artists'])
        numArtistsloaded = lt.size(listArtistsloaded)
        print('Artistas Cargados: ' + str(numArtistsloaded))
        print(lt.getElement(catalog["artworks"], 2))

    elif int(inputs[0]) == 2:

        a = 1

    elif int(inputs[0]) == 3:

        aninicial = input('Indique la fecha inicial de las obras que desea consultar en el formato AAAA-MM-DD (con los numeros menores a 10 como 01, 02, etc): ')
        afinal = input('Indique la fecha final de las obras que desea consultar en el formato AAAA-MM-DD (con los numeros menores a 10 como 01, 02, etc): ')

        result = controller.sortArtworksByAdDate(catalog, aninicial, afinal)
        printSortedResults(result)

    elif int(inputs[0]) == 4:

        a = 1
    elif int(inputs[0]) == 5:

        result = controller.countArtworksNationality(catalog)

        printArtworksbyNationality(result)

    elif int(inputs[0]) == 6:

        department = input('Digite el departamento del cual desea calcular el costo del transporte: ')
        result = controller.moveDepartment(catalog, department)
        printMoveDepartment(result)

    elif int(inputs[0]) == 7:

        a = 1

    else:
        sys.exit(0)
sys.exit(0)
