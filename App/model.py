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


from os import name
from DISClib.DataStructures.arraylist import addLast, newList
from DISClib.DataStructures.chaininghashtable import get
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

    catalog['artists'] = mp.newMap(34000,
                                   maptype='PROBING',
                                   loadfactor=0.5,
                                   comparefunction=compareArtists)

    catalog['birthArtist'] = mp.newMap(1200,
                                       maptype='CHAINING',
                                       loadfactor=4.0,
                                       comparefunction=compareBirthArtist)

    catalog['nationality'] = mp.newMap(200,
                                       maptype='CHAINING',
                                       loadfactor=4.0,
                                       comparefunction=compareNationality)

    catalog['artistID'] = mp.newMap(17000,
                                    maptype='CHAINING',
                                    loadfactor=0.8,
                                    comparefunction=compareArtistsID)

    catalog['adDate'] = mp.newMap(40000,
                                  maptype='CHAINING',
                                  loadfactor=4.0,
                                  comparefunction=compareArtworksByAdDAte)

    catalog['department'] = mp.newMap(1200,
                                      maptype='CHAINING',
                                      loadfactor=4.0,
                                      comparefunction=compareArtworksByDepartment)

    catalog['numberNationality'] = mp.newMap(500,
                                             maptype='CHAINING',
                                             loadfactor=4.0,
                                             comparefunction=compareCountryByNumberOfArtworks)

    return catalog


# Funciones para agregar informacion al catalogo


def addInfoArtist(catalog, name, constituentid, nationality, begindate, enddate, gender):
    # Creacion de tabla artistID y artists
    if mp.contains(catalog['artistID'], constituentid) is False:
        mp.put(catalog['artistID'], constituentid, name)
        artist = {}
        artist['Nationality'] = nationality
        artist['BeginDate'] = begindate
        artist['EndDate'] = enddate
        artist['Gender'] = gender
        lstArtistArtworks = lt.newList('ARRAY_LIST')
        artist['Artworks'] = lstArtistArtworks
        mp.put(catalog['artists'], name, artist)

    # Creacion de tabla birthArtist
    if mp.contains(catalog['birthArtist'], begindate) is False:
        lstBirthArtist = lt.newList("ARRAY_LIST")
        birthArtist = {}
        birthArtist['name'] = name
        birthArtist['BeginDate'] = begindate
        birthArtist['EndDate'] = enddate
        birthArtist['Gender'] = gender
        birthArtist['Nationality'] = nationality
        lt.addLast(lstBirthArtist, birthArtist)
        mp.put(catalog['birthArtist'], begindate, lstBirthArtist)

    else:
        birthArtist = {}
        entryBirthArtist = mp.get(catalog['birthArtist'], begindate)
        lstBirthArtist = me.getValue(entryBirthArtist)
        birthArtist['name'] = name
        birthArtist['BeginDate'] = begindate
        birthArtist['EndDate'] = enddate
        birthArtist['Gender'] = gender
        birthArtist['Nationality'] = nationality
        lt.addLast(lstBirthArtist, birthArtist)


def addArtwork(catalog, title, dateAcquired, lstmedium, dimensions, lstconstituentid,
               objectid, creditline, date, classification, height, width, department, length, weight):

    dictArtwork = newArtwork(title)
    dictArtwork['DateAcquired'] = dateAcquired
    dictArtwork['Dimensions'] = dimensions
    dictArtwork['ObjectID'] = objectid
    dictArtwork['ArtistsID'] = lstconstituentid
    dictArtwork['CreditLine'] = creditline
    dictArtwork['Date'] = date
    dictArtwork['Medium'] = lstmedium
    dictArtwork['Classification'] = classification
    dictArtwork['Height (cm)'] = height
    dictArtwork['Width (cm)'] = width
    dictArtwork['Department'] = department
    dictArtwork['Length (cm)'] = length
    dictArtwork['Weight (kg)'] = weight
    dictArtwork['Artists'] = lstconstituentid
    lt.addLast(catalog['artworks'], dictArtwork)

    # Creacion tabla nacionalidad
    for cID in lstconstituentid:
        lstArtworksCountry = lt.newList('ARRAY_LIST')
        if mp.contains(catalog['artistID'], cID):
            entryID = mp.get(catalog['artistID'], cID)
            name = me.getValue(entryID)
            entryNationality = mp.get(catalog['artists'], name)
            nationality = (me.getValue(entryNationality))['Nationality']

            if mp.contains(catalog['nationality'], nationality) is False:
                dictTArtwork = {}
                dictTArtwork['Title'] = title
                dictTArtwork['Date'] = date
                dictTArtwork['Medium'] = lstmedium
                dictTArtwork['Dimensions'] = dimensions
                dictTArtwork['Artists'] = lstconstituentid
                lt.addLast(lstArtworksCountry, dictTArtwork)
                mp.put(catalog['nationality'], nationality, lstArtworksCountry)

            else:
                entry = mp.get(catalog['nationality'], nationality)
                lstArtworksCountry = me.getValue(entry)
                dictTArtwork = {}
                dictTArtwork['Title'] = title
                dictTArtwork['Date'] = date
                dictTArtwork['Medium'] = lstmedium
                dictTArtwork['Dimensions'] = dimensions
                dictTArtwork['Artists'] = lstconstituentid
                lt.addLast(lstArtworksCountry, dictTArtwork)

        # Se agrega la obra de los artistas al map de artistas
        entryIDname = mp.get(catalog['artistID'], cID)
        IDname = me.getValue(entryIDname)
        entryLstArtworks = mp.get(catalog['artists'], IDname)
        dictArtist = me.getValue(entryLstArtworks)
        dictArtw = {}
        dictArtw['Title'] = title
        dictArtw['Date'] = date
        dictArtw['Medium'] = lstmedium
        dictArtw['Dimensions'] = dimensions
        dictArtw['DateAcquired'] = dateAcquired
        dictArtw['Department'] = department
        dictArtw['Dimensions'] = dimensions
        dictArtw['Classification'] = classification
        lt.addLast(dictArtist['Artworks'], dictArtw)

    # Creacion tabla adDate de obras
    if mp.contains(catalog['adDate'], dateAcquired) is False:
        lstadDate = lt.newList("ARRAY_LIST")
        adDate = {}
        adDate['Title'] = title
        adDate['Date'] = date
        adDate['Medium'] = lstmedium
        adDate['Dimensions'] = dimensions
        adDate['CreditLine'] = creditline
        lstArtworkArtists = lt.newList('ARRAY_LIST')
        for cID in lstconstituentid:
            entrycID = mp.get(catalog['artistID'], cID)
            nameArtist = me.getKey(entrycID)
            lt.addLast(lstArtworkArtists, nameArtist)
        adDate['Artists'] = lstArtworkArtists
        lt.addLast(lstadDate, adDate)
        mp.put(catalog['adDate'], dateAcquired, lstadDate)

    else:
        adDate = {}
        entryadDate = mp.get(catalog['adDate'], dateAcquired)
        lstadDate = me.getValue(entryadDate)
        adDate['Title'] = title
        adDate['Date'] = date
        adDate['Medium'] = lstmedium
        adDate['Dimensions'] = dimensions
        adDate['CreditLine'] = creditline
        lstArtworkArtists = lt.newList('ARRAY_LIST')
        for cID in lstconstituentid:
            entrycID = mp.get(catalog['artistID'], cID)
            nameArtist = me.getValue(entrycID)
            lt.addLast(lstArtworkArtists, nameArtist)
        adDate['Artists'] = lstArtworkArtists
        lt.addLast(lstadDate, adDate)

    # Creacion tabla department obras
    if mp.contains(catalog['department'], department) is False:
        lstDepartment = lt.newList('ARRAY_LIST')
        dep = {}
        dep['Title'] = title
        dep['Date'] = date
        dep['Classification'] = classification
        dep['Medium'] = lstmedium
        dep['Dimensions'] = dimensions
        dep['Height (cm)'] = height
        dep['Width (cm)'] = width
        dep['Weight (kg)'] = weight
        dep['Length (cm)'] = length
        lt.addLast(lstDepartment, dep)
        mp.put(catalog['department'], department, lstDepartment)

    else:
        dep = {}
        entryDep = mp.get(catalog['department'], department)
        lstDepartment = me.getValue(entryDep)
        dep['Title'] = title
        dep['Date'] = date
        dep['Classification'] = classification
        dep['Medium'] = lstmedium
        dep['Dimensions'] = dimensions
        dep['Height (cm)'] = height
        dep['Width (cm)'] = width
        dep['Weight (kg)'] = weight
        dep['Length (cm)'] = length
        lstArtworkArtists = lt.newList('ARRAY_LIST')
        for cID in lstconstituentid:
            entrycID = mp.get(catalog['artistID'], cID)
            nameArtist = me.getValue(entrycID)
            lt.addLast(lstArtworkArtists, nameArtist)
        dep['Artists'] = lstArtworkArtists
        lt.addLast(lstDepartment, dep)


# Funciones para creacion de datos


def newArtwork(title):
    artwork = {'Title': "", 'DateAcquired': 0, 'ArtistsID': None, 'Medium': None,
               'Dimensions': "", 'ObjectID': 0, "CreditLine": "", "Artists": [], 'Date': "",
               'Classification': "", 'Height (cm)': 0, 'Width (cm)': 0, 'Department': "", 'Length (cm)': 0, 'Weight (kg)': 0}
    artwork['Title'] = title

    return artwork


# Funciones de consulta
def sortArtists (catalog, year1,year2):
    yearkeys = mp.keySet(catalog['birthArtist'])
    yearlist = lt.newList('ARRAY_LIST')

    for year in lt.iterator(yearkeys):
        if cmpArtistbyBirthDate(year1, year) is True:
            if cmpArtistbyBirthDate(year, year2) is True:
                lt.addLast(yearlist, year)

    sub_list = yearlist.copy()
    sorted_list = None
    sorted_list = ms.sort(sub_list,cmpArtistbyBirthDate)
    totalArtists = 0
    listaFinal=lt.newList('ARRAY_LIST')
    for x in lt.iterator(sorted_list):
        entryData = mp.get(catalog['birthArtist'],x)
        data = me.getValue(entryData)
        for y in lt.iterator(data):
            d = {}
            d['Nombre'] = y['name']
            if y ['BeginDate'] == '0':
                d['año de nacimiento'] = 'no se sabe'
            else:
                d['año de nacimiento'] = y['BeginDate']
            if y['EndDate'] == '0':
                d['año de fallecimiento'] = ''
            else:
                d['año de fallecimiento'] = y['EndDate']

            d['Nacionalidad'] = y['Nationality']
            d['Género'] = y['Gender']
            lt.addLast(listaFinal,d)
            totalArtists += 1
    return (listaFinal, totalArtists)

def sortArtworksByAdDate(catalog, d1, d2):

    dateLst = mp.keySet(catalog['adDate'])
    finalDateLst = lt.newList('ARRAY_LIST')
    for date in lt.iterator(dateLst):
        if cmpArtworkByDateAcquired(d1, date) is True:
            if cmpArtworkByDateAcquired(date, d2) is True:
                lt.addLast(finalDateLst, date)

    sub_list = finalDateLst.copy()
    sorted_list = None
    sorted_list = ms.sort(sub_list, cmpArtworkByDateAcquired)

    totalArtworks = 0
    totalPurchasedartworks = 0
    lstFinal = lt.newList('ARRAY_LIST')
    for element in lt.iterator(sorted_list):
        entryData = mp.get(catalog['adDate'], element)
        data = me.getValue(entryData)
        adDate = me.getKey(entryData)
        dicT = {}
        for lstElement in lt.iterator(data):
            dicT['Title'] = lstElement['Title']
            dicT['DateAcquired'] = adDate
            dicT['Date'] = lstElement['Date']
            dicT['Artists'] = lstElement['Artists']
            dicT['Medium'] = lstElement['Medium']
            dicT['Dimensions'] = lstElement['Dimensions']
            lt.addLast(lstFinal, dicT)
            totalArtworks += 1
            if 'Purchase' in lstElement['CreditLine']:
                totalPurchasedartworks += 1

    return lstFinal, totalArtworks, totalPurchasedartworks

def classifyArtists (catalog, name):
    total_obras = 0
    total_medios = 0
    artists = mp.keySet(catalog['artists'])
    for x in lt.iterator(artists):
        if x == name:
            total_obras += 1
            valores = mp.get(catalog['artists'],x)
            v = me.getValue(valores)
    total_obras = lt.size (v['Artworks'])
    
    lista_medios = lt.newList('ARRAY_LIST')
    for i in lt.iterator(v['Artworks']):
        lt.addLast(lista_medios,i['Medium']) 
    
    sub_list = lista_medios.copy()
    sorted_list = None
    sorted_list = ms.sort(sub_list,cmpartistsbymedium)
    lista_prueba = lt.newList('ARRAY_LIST')
    for j in lt.iterator(sorted_list):
        if (lt.isPresent (lista_prueba, j)) == 0:
            total_medios +=1
            lt.addLast(lista_prueba,j)




    
def countArtworksByNationality(catalog):

    countries = mp.keySet(catalog['nationality'])
    lstNumbers = lt.newList('ARRAY_LIST')
    for country in lt.iterator(countries):
        if (len(country) > 0 and (country
         != 'Nationality unknown')):
            entryCountry = mp.get(catalog['nationality'], country)
            lstCountry = me.getValue(entryCountry)
            numberArtworksCountry = lt.size(lstCountry)
            mp.put(catalog['numberNationality'], numberArtworksCountry, country)
            lt.addLast(lstNumbers, numberArtworksCountry)

    sorted_list = None
    sorted_list = ms.sort(lstNumbers, cmpCountriesbyArtworks)

    lstOrd = lt.newList('ARRAY_LIST')
    for number in lt.iterator(sorted_list):
        ordDict = {}
        entryNumber = mp.get(catalog['numberNationality'], number)
        countryNumber = me.getValue(entryNumber)
        ordDict[countryNumber] = number
        lt.addLast(lstOrd, ordDict)

    # Datos de las obras TOP 1
    topCountryDic = lt.getElement(lstOrd, 1)
    topCountryLst = list(topCountryDic.keys())
    topCountry = topCountryLst[0]
    checkList = []
    lstData = lt.newList('ARRAY_LIST')
    entryTopCountry = mp.get(catalog['nationality'], topCountry)
    lstArtworksTopCountry = me.getValue(entryTopCountry)
    for artwork in lt.iterator(lstArtworksTopCountry):
        dictData = {}
        lstArtists = lt.newList('ARRAY_LIST')
        if artwork['Title'] not in checkList:
            for artist in artwork['Artists']:
                artistNameEntry = mp.get(catalog['artistID'], artist)
                artistName = me.getValue(artistNameEntry)
                lt.addLast(lstArtists, artistName)

            dictData['Title'] = artwork['Title']
            dictData['Artists'] = lstArtists
            dictData['Date'] = artwork['Date']
            dictData['Medium'] = artwork['Medium']
            dictData['Dimensions'] = artwork['Dimensions']
            lt.addLast(lstData, dictData)

    return lstOrd, lstData


def moveDepartment(catalog, department):

    entryDepartment = mp.get(catalog['department'], department)
    lstDepartment = me.getValue(entryDepartment)
    totalPrice = 0
    totalWeight = 0
    for artwork in lt.iterator(lstDepartment):
        area = 0
        volume = 0
        weight = 0
        p1 = 0
        p2 = 0
        p3 = 0
        may = 0
        area = (artwork['Height (cm)'] * artwork['Width (cm)'])/10000
        volume = (artwork['Height (cm)'] * artwork['Width (cm)'] * artwork['Length (cm)'])/1000000
        weight = artwork['Weight (kg)']
        p1 = area * 72
        p2 = volume * 72
        p3 = weight * 72

        if p1 > p2:
            may = p1

        else:
            p2 = may

        if p3 > may:
            may = p3

        if may == 0:
            may = 48

        artwork['Price'] = may
        totalPrice += may
        totalWeight += weight

    ltsize = lt.size(lstDepartment)
    sub_list = lt.subList(lstDepartment, 1, ltsize)
    sub_list = sub_list.copy()
    sortedDate_list = None
    sortedDate_list = ms.sort(sub_list, cmpArtworkByDateSort)
    sub_list2 = lt.subList(lstDepartment, 1, ltsize)
    sub_list2 = sub_list2.copy()
    sortedPrice_list = None
    sortedPrice_list = ms.sort(sub_list2, cmpArtworkByPrice)

    return totalPrice, totalWeight, sortedDate_list, sortedPrice_list


def findBestArtists(catalog, n, a1, a2):

    artists = mp.keySet(catalog['artists'])
    sortLst = lt.newList('ARRAY_LIST')
    for artist in lt.iterator(artists):
        sortList = []
        artistDicEntry = mp.get(catalog['artists'], artist)
        artistDic = me.getValue(artistDicEntry)  
        if int(artistDic['BeginDate']) >= int(a1):
            if int(artistDic['BeginDate']) <= int(a2):
                sortList.append(lt.size(artistDic['Artworks']))
                checklist = {}
                for artwork in lt.iterator(artistDic['Artworks']):
                    for medium in artwork['Medium']:
                        if medium not in list(checklist.keys()):
                            checklist[medium] = 1

                        else:
                            checklist[medium] += 1

                sortList.append(len(list(checklist.keys())))
                dictSortList = {}
                dictSortList[artist] = sortList
                lt.addLast(sortLst, dictSortList)

    ltsize = lt.size(sortLst)
    sub_list = lt.subList(sortLst, 1, ltsize)
    sub_list = sub_list.copy()
    sorted_list = None
    sorted_list = ms.sort(sub_list, cmpArtworksByCond)
    crop_list = lt.subList(sorted_list, 1, n)

    # Datos de los artistas
    lstFinalArtists = lt.newList('ARRAY_LIST')
    for artist in lt.iterator(crop_list):
        artistName = (list(artist.keys()))[0]
        dictFinal = {}
        dictFinal['Name'] = artistName
        dictFinal['TotalArtworks'] = (artist[artistName])[0]
        dictFinal['TotalMediums'] = (artist[artistName])[1]
        specificArtistEntry = mp.get(catalog['artists'], artistName)
        specificArtist = me.getValue(specificArtistEntry)
        dictFinal['Gender'] = specificArtist['Gender']
        dictFinal['BeginDate'] = specificArtist['BeginDate']
        dictCheck = {}
        # Busqueda de la tecnica favorita
        for artwork in lt.iterator(specificArtist['Artworks']):
            lstMediums = artwork['Medium']
            for medium in lstMediums:
                if medium not in (list(dictCheck.keys())):
                    dictCheck[medium] = 1
                else:
                    dictCheck[medium] += 1

        maxElement = max(list(dictCheck.values()))
        posMaxElement = (list(dictCheck.values())).index(maxElement)
        favMedium = (list(dictCheck.keys()))[posMaxElement]
        dictFinal['FavoriteMedium'] = favMedium
        lt.addLast(lstFinalArtists, dictFinal)

    # 5 obras de top artist
    topArtist = lt.getElement(lstFinalArtists, 1)
    topArtistName = topArtist['Name']
    lstTopArtistArtworks = lt.newList('ARRAY_LIST')
    topArtistDictEntry = mp.get(catalog['artists'], topArtistName)
    topArtistDict = me.getValue(topArtistDictEntry)
    for artwork in lt.iterator(topArtistDict['Artworks']):
        dictArtwork = {}
        if topArtist['FavoriteMedium'] in artwork['Medium']:
            dictArtwork['Title'] = artwork['Title']
            dictArtwork['Date'] = artwork['Date']
            dictArtwork['DateAcquired'] = artwork['DateAcquired']
            dictArtwork['Medium'] = artwork['Medium']
            dictArtwork['Department'] = artwork['Department']
            dictArtwork['Classification'] = artwork['Classification']
            dictArtwork['Dimensions'] = artwork['Dimensions']
            lt.addLast(lstTopArtistArtworks, dictArtwork)

        if lt.size(lstTopArtistArtworks) == 5:
            break

    return lstFinalArtists, lstTopArtistArtworks


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


def compareBirthArtist(keyname, birthdate):
    birthEntry = me.getKey(birthdate)
    if (keyname == birthEntry):
        return 0
    elif (keyname > birthEntry):
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


def compareArtworksByAdDAte(keyname, adDate):
    dateEntry = me.getKey(adDate)
    if (keyname == dateEntry):
        return 0
    elif (keyname > dateEntry):
        return 1
    else:
        return -1


def compareArtworksByDepartment(keyname, department):
    depEntry = me.getKey(department)
    if (keyname == depEntry):
        return 0
    elif (keyname > depEntry):
        return 1
    else:
        return -1


def compareCountryByNumberOfArtworks(keyname, department):
    depEntry = me.getKey(department)
    if (keyname == depEntry):
        return 0
    elif (keyname > depEntry):
        return 1
    else:
        return -1


def compareCountryByBestArtists(keyname, department):
    depEntry = me.getKey(department)
    if (keyname == depEntry):
        return 0
    elif (keyname > depEntry):
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

def cmpartistsbymedium (medium1,medium2):
    r = None
    if medium1 >= medium2:
        r = True
    else:
        r = False
    return r

def cmpCountriesbyArtworks(country1, country2):

    r = None
    if country1 > country2:
        r = True
    else:
        r = False

    return r

def cmpArtistbyBirthDate(date1, date2):
    r = None

    if (int(date1)) <= (int(date2)):
        r = True
    else:
        r = False
    return r

def cmpArtworkByDateAcquired(artwork1, artwork2):
    """ Devuelve verdadero (True) si el 'DateAcquired' de artwork1 es menores que el de artwork2
        Args:
            artwork1: informacion de la primera obra que incluye su valor 'DateAcquired' 
            artwork2: informacion de la segunda obra que incluye su valor 'DateAcquired' 
    """
    date1 = artwork1.split("-")
    date2 = artwork2.split("-")
    r = None
    if (len(date1) < 2):
        date1 = [2021, 10, 20]
        artwork1 = '2021-10-02'
    if (len(date2)) < 2:
        date2 = [2021, 10, 20]
        artwork2 = '2021-10-02'
    
    if int(date1[0]) < int(date2[0]):
        r = True
    elif int(date1[0]) > int(date2[0]):
        r = False
    elif int(date1[1]) < int(date2[1]):
        r = True
    elif int(date1[1]) > int(date2[1]):
        r = False
    elif int(date1[2]) < int(date2[2]):
        r = True
    elif int(date1[2]) > int(date2[2]):
        r = False

    return r


def cmpArtworkByDateSort(artwork1, artwork2):

    if artwork1['Date'] == '':
        date1 = 2021
        artwork1['Date'] = 2021
    else:
        date1 = int(artwork1['Date'])

    if artwork2['Date'] == '':
        date2 = 2021
        artwork2['Date'] = 2021
    else:
        date2 = int(artwork2['Date'])

    if date1 < date2:
        r = True
    else:
        r = False

    return r


def cmpArtworkByPrice(artwork1, artwork2):

    if artwork1['Price'] < artwork2['Price']:
        r = True
    else:
        r = False
    return r


def cmpArtworksByCond(artist1, artist2):

    nameList1 = list(artist1.keys())
    name1 = nameList1[0]
    nameList2 = list(artist2.keys())
    name2 = nameList2[0]
    if artist1[name1][0] < artist2[name2][0]:
        r = False
    elif artist1[name1][0] > artist2[name2][0]:
        r = True
    elif artist1[name1][1] < artist2[name2][1]:
        r = False
    elif artist1[name1][1] > artist2[name2][1]:
        r = True
    else:
        r = True
    return r
