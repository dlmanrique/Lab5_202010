"""
 * Copyright 2020, Departamento de sistemas y Computación, Universidad de Los Andes
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
 * along with this program.  If not, see <http://www.gnu.org/licenses/>.
 """


import config as cf
from ADT import list as lt
from ADT import orderedmap as tree
from ADT import map as map
from ADT import list as lt
from DataStructures import listiterator as it
from datetime import datetime

"""
Se define la estructura de un catálogo de libros.
El catálogo tendrá tres listas, una para libros, otra para autores 
y otra para géneros
"""

# Construccion de modelos



def newCatalog():
    """
    Inicializa el catálogo y retorna el catalogo inicializado.
    """
    catalog = {'dateTree':None, 'accidentsList':None}
    #implementación de Black-Red Tree (brt) por default
    catalog['dateTree'] = tree.newMap()
    catalog['accidentsList'] = lt.newList("ARRAY_LIST")
    return catalog





def newDate (date, row):
    """
    Crea una nueva estructura para almacenar los accidentes por fecha 
    """
    dateNode = {"date": date, "severityMap":None}
    dateNode ['severityMap'] = map.newMap(7,maptype='CHAINING')
    intSeverity = int(row['Severity'])
    map.put(dateNode['severityMap'],intSeverity,1, compareByKey)
    return dateNode



def addDateTree (catalog, row):
    """
    Adiciona el libro al arbol anual key=original_publication_year
    """
    DateText= row['Start_Time']     
    DateText = DateText[0:10]  
    date = strToDate(DateText,'%Y-%m-%d')
    dateNode = tree.get(catalog['dateTree'], date, greater)
    if dateNode:
        severity = int(row['Severity'])
        severityCount = map.get(dateNode['severityMap'], severity, compareByKey)
        if  severityCount:
            severityCount+=1
            map.put(dateNode['severityMap'], severity, severityCount, compareByKey)
        else:
            map.put(dateNode['severityMap'], severity, 1, compareByKey)
    else:
        dateNode = newDate(date,row)
        tree.put(catalog['dateTree'],date,dateNode,greater)
        



# Funciones de consulta






def getAccidentByDateSeverity (catalog, date):
    """
    Retorna la cantidad de libros para un año y con un rating dado
    """
    
    dateElement = tree.get(catalog['dateTree'], strToDate(date,'%Y-%m-%d') , greater)
    response=''
    if dateElement:
        ratingList = map.keySet(dateElement['severityMap'])
        iteraRating=it.newIterator(ratingList)
        while it.hasNext(iteraRating):
            ratingKey = it.next(iteraRating)
            response += 'Severity '+str(ratingKey) + ':' + str(map.get(dateElement['severityMap'],ratingKey,compareByKey)) + '\n'
        return response
    return None
# Funciones de comparacion

def compareByKey (key, element):
    return  (key == element['key'] )  

def compareByTitle(bookTitle, element):
    return  (bookTitle == element['title'] )

def greater (key1, key2):
    if ( key1 == key2):
        return 0
    elif (key1 < key2):
        return -1
    else:
        return 1

def strToDate(date_string, format):
    
    try:
        # date_string = '2016/05/18 13:55:26' -> format = '%Y/%m/%d %H:%M:%S')
        return datetime.strptime(date_string,format)
    except:
        return datetime.strptime('1900', '%Y')

