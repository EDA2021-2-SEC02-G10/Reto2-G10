"""
 * Copyright 2020, Departamento de sistemas y Computación,
 * Universidad de Los Andes
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
 *
 * Contribuciones:
 *
 * Dario Correal - Version inicial
 """


import config as cf
from DISClib.ADT import list as lt
from DISClib.ADT import map as mp
from DISClib.DataStructures import mapentry as me
from DISClib.Algorithms.Sorting import mergesort as ms
assert cf

"""
Se define la estructura de un catálogo de videos. El catálogo tendrá dos listas, una para los videos, otra para las categorias de
los mismos.
"""

# Construccion de modelos


def newCatalog():
    """

    """
    catalog = {'artworks': None,
               'artists': None,
               'medium': None,
               'nationality': None,
               'artistId': None}

    catalog['artworks'] = lt.newList('ARRAY_LIST', cmpfunction=compareArtworks)

    catalog['artists'] = mp.newMap(1200,
                                   maptype='CHAINING',
                                   loadfactor=4.0,
                                   comparefunction=compareArtists)

    catalog['medium'] = mp.newMap(1200,
                                  maptype='CHAINING',
                                  loadfactor=4.0,
                                  comparefunction=compareMedium)

    catalog['nationality'] = mp.newMap(1200,
                                       maptype='CHAINING',
                                       loadfactor=4.0,
                                       comparefunction=compareNationality)

    catalog['artistID'] = mp.newMap(1200,
                                    maptype='CHAINING',
                                    loadfactor=0.8,
                                    comparefunction=compareArtistsID)

    return catalog


# Funciones para agregar informacion al catalogo


def addInfoArtist(catalog, name, constituentid, nationality, begindate, enddate, gender):

    if mp.contains(catalog['artistID'], constituentid) is False:
        mp.put(catalog['artistID'], constituentid, name)
        artist = {}
        artist['Nationality'] = nationality
        artist['BeginDate'] = begindate
        artist['EndDate'] = enddate
        artist['Gender'] = gender
        mp.put(catalog['artists'], name, artist)


def addArtwork(catalog, title, dateAcquired, lstmedium, dimensions, lstconstituentid,
               objectid, creditline, date, classification, height, width, department, length, weight):

    dictArtwork = newArtwork(title)
    dictArtwork['DateAcquired'] = dateAcquired
    dictArtwork['Dimensions'] = dimensions
    dictArtwork['ObjectID'] = objectid
    dictArtwork['ArtistsID'] = lstconstituentid
    dictArtwork['CreditLine'] = creditline
    dictArtwork['Date'] = date
    dictArtwork['Classification'] = classification
    dictArtwork['Height (cm)'] = height
    dictArtwork['Width (cm)'] = width
    dictArtwork['Department'] = department
    dictArtwork['Length (cm)'] = length
    dictArtwork['Weight (kg)'] = weight
    lt.addLast(catalog['artworks'], dictArtwork)

    # Creacion de la tabla de hash de medios
    for medium in lstmedium:
        dictTD = {}
        if mp.contains(catalog['medium'], medium) is False:
            listMedium = lt.newList('ARRAY_LIST')
            dictTD['Title'] = dictArtwork['Title']
            dictTD['Date'] = dictArtwork['Date']
            lt.addLast(listMedium, dictTD)
            mp.put(catalog['medium'], medium, listMedium)
        else:
            entryMap = mp.get(catalog['medium'], medium)
            valueMap = me.getValue(entryMap)
            dictTD['Title'] = dictArtwork['Title']
            dictTD['Date'] = dictArtwork['Date']
            lt.addLast(valueMap, dictTD)

    # Creacion tabla nacionalidad
    for cID in lstconstituentid:
        lstArtworksCountry = lt.newList('ARRAY_LIST')
        if mp.contains(catalog['artistID'], cID):
            entryID = mp.get(catalog['artistID'], cID)
            name = me.getValue(entryID)
            entryNationality = mp.get(catalog['artists'], name)
            nationality = (me.getValue(entryNationality))['Nationality']

            if mp.contains(catalog['nationality'], nationality) is False:
                lt.addLast(lstArtworksCountry, title)
                mp.put(catalog['nationality'], nationality, lstArtworksCountry)
            else:
                entry = mp.get(catalog['nationality'], nationality)
                lstArtworksCountry = me.getValue(entry)
                lt.addLast(lstArtworksCountry, title)


# Funciones para creacion de datos


def newArtist(constituentid):

    artist = {'name': "", 'ConstituentID': "", 'Nationality': "", "artworks": None, 'BeginDate':0, 'EndDate':0, 'Gender':""}
    artist['ConstituentID'] = constituentid
    artist['artworks'] = lt.newList('ARRAY_LIST')

    return artist


def newArtwork(title):
    artwork = {'Title': "", 'DateAcquired': 0, 'ArtistsID': None, 'Medium': None,
               'Dimensions': "", 'ObjectID': 0, "CreditLine": "", "Artists": [], 'Date': "",
               'Classification': "", 'Height (cm)': 0, 'Width (cm)': 0, 'Department': "", 'Length (cm)': 0, 'Weight (kg)': 0}
    artwork['Title'] = title

    return artwork


# Funciones de consulta


def findOldestArtworks(catalog, n, medium):

    entryArtworksMedium = mp.get(catalog['medium'], medium)
    lstArtworksMedium = me.getValue(entryArtworksMedium)
    lstSize = lt.size(lstArtworksMedium)
    sub_list = lt.subList(lstArtworksMedium, 1, lstSize)
    sorted_list = ms.sort(sub_list, cmpArtworksByDate)
    lstFinal = lt.subList(sorted_list, 1, n)

    return lstFinal


def countArtworksNationality(catalog, nationality):

    entryArtworksNationality = mp.get(catalog['nationality'], nationality)
    lstArtworksNationality = me.getValue(entryArtworksNationality)
    nArtworks = lt.size(lstArtworksNationality)

    return nArtworks

# Funciones utilizadas para comparar elementos dentro de una lista


def compareArtists(keyname, artist):
    artistEntry = me.getKey(artist)
    if (keyname == artistEntry):
        return 0
    elif (keyname > artistEntry):
        return 1
    else:
        return -1


def compareArtworks(artworkid, artwork):
    if artworkid in artwork['ArtistsID']:
        return 0
    return -1


def compareMedium(keyname, medium):
    mediumEntry = me.getKey(medium)
    if (keyname == mediumEntry):
        return 0
    elif (keyname > mediumEntry):
        return 1
    else:
        return -1


def compareArtistsID(keyname, cID):
    cIDEntry = me.getKey(cID)
    if (keyname == cIDEntry):
        return 0
    elif (keyname > cIDEntry):
        return 1
    else:
        return -1


def compareNationality(keyname, nationality):
    nationalityEntry = me.getKey(nationality)
    if (keyname == nationalityEntry):
        return 0
    elif (keyname > nationalityEntry):
        return 1
    else:
        return -1


# Funciones de ordenamiento


def cmpArtworksByDate(artwork1, artwork2):

    r = None
    date1 = artwork1['Date']
    date2 = artwork2['Date']
    if date1 == '':
        date1 = 2021

    if date2 == '':
        date2 = 2021

    if int(date1) < int(date2):
        r = True
    else:
        r = False
    return r
