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

#from DISClib.DataStructures.chaininghashtable import keySet
import config as cf
import controller
from DISClib.ADT import list as lt
from DISClib.ADT import map as mp
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


def printMenu():
    print("Bienvenido")
    print("1- Cargar información en el catálogo")
    print("2- Encontrar las n obras mas antiguas de un medio")
    print("3- Encontrar el numero de obras de una nacionalidad")


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
        listArtistsloaded = mp.keySet(catalog['nationality'])
        numArtistsloaded = lt.size(listArtistsloaded)
        print('Artistas Cargados: ' + str(numArtistsloaded))
        print(lt.getElement(catalog["artworks"], 2))
        print(lt.size(mp.keySet(catalog['nationality'])))

    elif int(inputs[0]) == 2:

        mediumArtworks = input('Digite el medio del cual desea encontrar las obras mas antiguas: ')
        numberArtworks = int(input('Digite el numero de obras mas antiguas que desea ver para dicho medio: '))
        result = controller.findOldestArtworks(catalog, numberArtworks, mediumArtworks)
        print('Las ' + str(numberArtworks) + ' obras mas viejas del medio ' + str(mediumArtworks) + 'son: ')
        print(result)

    elif int(inputs[0]) == 3:

        inputNationality = input("Digite la nacionalidad de la cual desea consultar su numero de obras: ")
        result = controller.countArtworksNationality(catalog, inputNationality)
        print('La nacionalidad mencionada tiene: ' + str(result) + ' obras registradas en el MOMA')

    else:
        sys.exit(0)
sys.exit(0)