import xml.etree.ElementTree as ET
import configparser
import os
from nltk.corpus import stopwords
from nltk.stem import SnowballStemmer
import nltk
import re
import pickle
import collections

ig = configparser.ConfigParser()
archivo = ig.read("config.ini")
diarios = ig.sections()
stemmer = SnowballStemmer("spanish")
descripcion = []
ultimoDocID = 0
ultimoTermID = 0

# GENERA DICCIONARIO DOCID->DOC A PARTIR DE DICCIONARIO DE DOC->STRING(TERMINOS)
def construirDocID(diccionarioDeDocs):
    diccionarioTemporal={}
    global ultimoDocID
    x=0
    values = list(diccionarioDeDocs.values()) 
    for i in range(1 + ultimoDocID,len(diccionarioDeDocs.keys())+ultimoDocID+1):
        diccionarioTemporal[i]=values[x]
        x=x+1
    ultimoDocID=ultimoDocID+len(diccionarioDeDocs.keys())
    return diccionarioTemporal


# GENERA DICCIONARIO TERMID->TERM A PARTIR DE LISTA DE PALABRAS STEMMEADAS
def construirTermID(palabras_stemmeadas):
    diccionarioTemporal={}
    global ultimoTermID
    x=0
    for i in range(1 + ultimoTermID,len(palabras_stemmeadas)+ultimoTermID+1):
        if palabras_stemmeadas[x] in diccionarioTemporal:
            pass
        else:
            diccionarioTemporal[i]=palabras_stemmeadas[x]
        x=x+1
    ultimoTermID=ultimoTermID+len(palabras_stemmeadas)
    return diccionarioTemporal    


# DEVUELVE DICCIONARIO DE DOCUMENTO -> STRING(TERMINOS)
def parsear_bloque(num):
    diccionarioDeDocs={}

    for seccion in ig[diarios[num]]:
        if seccion != "query_interval" and seccion != "tmp" and seccion != "output" and seccion != "url_base":
            tree = ET.parse('out/'+diarios[num]+'/'+seccion+'/'+seccion+'.xml')
            root = tree.getroot()
            for item in root.findall("item"):
                descripcionTemporal=item.find('description')
                if descripcionTemporal == None:
                    pass
                else:
                    if descripcionTemporal.text != None:
                        if diarios[num]+"-"+seccion+"-"+item.find("title").text+item.find("pubDate").text in diccionarioDeDocs:
                            pass
                        else:
                            diccionarioDeDocs[diarios[num]+"-"+seccion+"-"+item.find("title").text+item.find("pubDate").text]=item.find("description").text
            return(diccionarioDeDocs)

# DEVUELVE LISTA DE PALABRAS STEMMEADAS EN EL DICCIONARIO DOCUMENTO -> STRING(TERMINOS)
def stemmear(diccionarioDeID):
    palabras_minuscula = []
    palabras_stemmeadas = []
    for key in diccionarioDeID:
        palabras = re.findall(r"[A-z]+[áéíóú]?[A-z]*", diccionarioDeID[key])
    
        for palabra in palabras:
            palabras_minuscula.append(palabra.lower())
    filtered_words = [word for word in palabras_minuscula if word not in stopwords.words('spanish') and not len(word) < 4]
    
    for word in filtered_words:
        if stemmer.stem(word) in palabras_stemmeadas:
            pass
        else:
            palabras_stemmeadas.append(stemmer.stem(word))  
    return(palabras_stemmeadas)


#GENERA DICCIONARIO TERMID->DOCID
def invertirDiccionario(diccionarioDeTermID, diccionarioDeDocID):

    dicInv={}
    for key in diccionarioDeDocID:
        textoBIENHECHO = diccionarioDeDocID[key].replace('"',"").lower()
        for numeroPalabra in diccionarioDeTermID: 
            if diccionarioDeTermID[numeroPalabra] in textoBIENHECHO:
                if numeroPalabra not in dicInv.keys():
                    dicInv[numeroPalabra]=[key]
                else:
                    dicInv[numeroPalabra].append(key)
    return(dicInv)

# GUARDA DICCIONARIO CON PICKLE
def guardarIndice(diccionarioAGuardar, numeroDeArchivo):
    with open("diccionario"+str(numeroDeArchivo)+".pickle","wb") as handle:
        pickle.dump(diccionarioAGuardar, handle, protocol=pickle.HIGHEST_PROTOCOL)

# RECUPERA DICICONARIO CON PICKLE
def recuperarIndice(diccionarioAEncontrar):
    with open(diccionarioAEncontrar+'.pickle', 'rb') as handle:
        b = pickle.load(handle)
    return b    

# ARCHIVO MAIN
def mainIndiceInvertido():
    diccionario = []
    for i in range(0,len(diarios)):
        print(diarios[i])
        bloqueParseado = parsear_bloque(i)
        diccionarioDocID = construirDocID(bloqueParseado)
        diccionarioTermID = construirTermID(stemmear(diccionarioDocID))
        diccionarioTemporal=invertirDiccionario(diccionarioTermID, diccionarioDocID)
        diccionario.append(dict(collections.OrderedDict(sorted(diccionarioTemporal.items()))))
        guardarIndice(diccionario[i],i)
        print(diccionario[i])
    return diccionario    

def encontrarIDdePalabra(palabra, diccionarioAEncontrar, diccionarioDeTerminosID):
    palabraStemmeada = stemmer.stem(palabra)
    for key in diccionarioAEncontrar:
        for termino in diccionarioDeTerminosID:
            if key == termino:
                if palabraStemmeada == diccionarioDeTerminosID[termino]:
                    if termino != None:
                        return(termino)


main = mainIndiceInvertido()
