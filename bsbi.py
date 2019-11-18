import xml.etree.ElementTree as ET
import configparser
import os
from nltk.corpus import stopwords
from nltk.stem import SnowballStemmer
import nltk
import re
import pickle
import collections
from UncompressedPostings import UncompressedPostings
import array
import sys
from termcolor import colored

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
        if palabras_stemmeadas[x] in list(diccionarioTemporal.values()):
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
                if descripcionTemporal != None:
                    if descripcionTemporal.text != None:
                        if item.find("title").text+ " " +item.find("description").text in diccionarioDeDocs.values():
                            pass
                        else:
                            diccionarioDeDocs[diarios[num]+"-"+seccion+"-"+item.find("title").text+item.find("pubDate").text]=item.find("title").text+ " " +item.find("description").text
    return(diccionarioDeDocs)

# DEVUELVE LISTA DE PALABRAS STEMMEADAS EN EL DICCIONARIO DOCUMENTO -> STRING(TERMINOS)
def stemmear(diccionarioDeID):
    palabras_minuscula = []
    palabras_stemmeadas = []
    for key in diccionarioDeID:
        palabras = re.findall(r"[A-z]+[áéíóú]?[A-z]*", diccionarioDeID[key].lower())
    
        for palabra in palabras:
            palabras_minuscula.append(palabra)
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
        texto = stemmer.stem(diccionarioDeDocID[key].replace('"',"").lower())
        for numeroPalabra in diccionarioDeTermID:
            if diccionarioDeTermID[numeroPalabra] in texto:
                if numeroPalabra not in dicInv.keys():
                    dicInv[numeroPalabra]=[key]
                else:
                    dicInv[numeroPalabra].append(key)
    return(dicInv)

#MERGEA DICICONARIO TERMID->DOCID

def mergearListaDeDiccionarios(diccionarioCompleto, dicTermID):
    diccionarioDePrueba = {}
    diccionarioNuevo = {}
    for key,value in dicTermID.items():
        if value not in diccionarioDePrueba:
            diccionarioDePrueba[value] = [key]
        else:
            diccionarioDePrueba[value].append(key)
    for key in diccionarioDePrueba:
        suma = []
        if len(diccionarioDePrueba[key]) > 1:
            for position in diccionarioDePrueba[key]:
                if position in diccionarioCompleto.keys():
                    suma = suma + diccionarioCompleto[position]
            if len(suma)!=0:        
                diccionarioNuevo[diccionarioDePrueba[key][0]] = suma
        else:
            if diccionarioDePrueba[key][0] in diccionarioCompleto.keys():
                diccionarioNuevo[diccionarioDePrueba[key][0]]= diccionarioCompleto[diccionarioDePrueba[key][0]]                
    return(diccionarioNuevo)    

  

        


# GUARDA DICCIONARIOS TERMID->TERM CON PICKLE
def guardarListaDeIndiceTermID(listaDeIndiceTermID):
    with open("out/diccionario_termid-term.pickle","wb") as handle:
        pickle.dump(listaDeIndiceTermID, handle, protocol=pickle.HIGHEST_PROTOCOL)    


# GUARDA DICCIONARIOS DOCID->STRING CON PICKLE
def guardarListaDeIndiceDocID(listaDeIndiceDocID):
    with open("out/diccionario_docid-doc.pickle","wb") as handle:
        pickle.dump(listaDeIndiceDocID, handle, protocol=pickle.HIGHEST_PROTOCOL)

# GUARDA INDICE INVERTIDO CON PICKLE
def guardarIndiceInvertido(diccionarioAGuardar):
    for i in range(0,len(diarios)):
        with open("out/"+diarios[i]+"/"+"diccionario_"+diarios[i]+".pickle","wb") as handle:
            pickle.dump(encodearDocs(diccionarioAGuardar[i]), handle, protocol=pickle.HIGHEST_PROTOCOL)        

# GUARDA DICCIONARIOS DOC->STRING CON PICKLE
def guardarListaDeIndiceDoc(listaDeIndiceDocID):
    with open("out/diccionario_doc-terms.pickle","wb") as handle:
        pickle.dump(listaDeIndiceDocID, handle, protocol=pickle.HIGHEST_PROTOCOL)            

# RECUPERA DICICONARIO CON PICKLE
def recuperarIndice():
    b=[]
    index = {}
    for i in range(0, len(diarios)):
        with open("out/"+diarios[i]+"/"+"diccionario_"+diarios[i]+".pickle", 'rb') as handle:
            b.append(decodearDocs(pickle.load(handle)))   
    for diccionario in b:
        for termid in diccionario:
            index[termid] = diccionario[termid]
    return index        

# RECUPERA DICICONARIO DOCID->DOC CON PICKLE
def recuperarListaDeIndiceDocID():
        with open("out/diccionario_docid-doc.pickle", 'rb') as handle:
            return pickle.load(handle)

# RECUPERA DICICONARIO DOC->STRING CON PICKLE
def recuperarListaDeIndiceDoc():
        with open("out/diccionario_doc-terms.pickle", 'rb') as handle:
            return pickle.load(handle)            

# RECUPERA DICICONARIO TERMID->TERM CON PICKLE
def recuperarListaDeIndiceTermID():
        with open("out/diccionario_termid-term.pickle", 'rb') as handle:
            return pickle.load(handle)
   

# ARCHIVO MAIN
def mainIndiceInvertido():
    diccionario = {}
    lista = []
    diccionarioNuevoDocID = {}
    diccionarioNuevoTermID = {}
    diccionarioDocTerm = {}
    newDict = {}
    for i in range(0,len(diarios)):
        print(diarios[i])
        bloqueParseado = parsear_bloque(i)
        for key in bloqueParseado:
            diccionarioDocTerm[key] = bloqueParseado[key]
        diccionarioDocID = construirDocID(bloqueParseado)
        for key in diccionarioDocID:
            diccionarioNuevoDocID[key]=diccionarioDocID[key]
        diccionarioTermID = construirTermID(stemmear(diccionarioDocID))
        for key in diccionarioTermID:
            diccionarioNuevoTermID[key]=diccionarioTermID[key]
        diccionarioTemporal=invertirDiccionario(diccionarioTermID, diccionarioDocID)
        lista.append(diccionarioTemporal)
        for key in diccionarioTemporal:
            diccionario[key]=diccionarioTemporal[key]   
        print(diccionarioTemporal)
    newDict=dict(collections.OrderedDict(sorted(diccionario.items())))
    guardarIndiceInvertido(lista) 
    guardarListaDeIndiceDoc(diccionarioDocTerm)
    guardarListaDeIndiceDocID(diccionarioNuevoDocID)
    guardarListaDeIndiceTermID(diccionarioNuevoTermID)
    return (newDict, lista)    


# ENCODEA DICCIONARIO INVERTIDO
def encodearDocs(dicInv):
    dicNuevo={}
    for key in dicInv:
        byteArray = UncompressedPostings.encode(dicInv[key])
        dicNuevo[key] = byteArray 
    return dicNuevo  

# DECODEA DICCIONARIO ENCODEADO
def decodearDocs(dicInvEncodeado):
    dicNuevo={}
    for key in dicInvEncodeado: 
        value = UncompressedPostings.decode(dicInvEncodeado[key])
        dicNuevo[key]=value
    return dicNuevo    

# COMPRIMIR EN BYTEARRAY UNA LISTA DE ENTEROS
def generar_value_de_term_id(dicInv):
    arrayTemp = []
    for key in dicInv:
        arrayTemp.append(key)
    return arrayTemp    

# METODO QUE CONVIERTE EL DICCIONARIO TERMID-DOCID
def generarArrayIDyDicConTupla(dic):

        dicTemporal = {}

        dicIntArray = []
        posicionInicial = 0
        cantidadDeDocs=0
        posicionActual = 0

        for termId in dic.keys():

            dicIntArray.append(termId)
            posicionActual = posicionActual +1

            for docId in dic.get(termId):

                dicIntArray.append(docId)

                cantidadDeDocs =cantidadDeDocs+1
                posicionActual = posicionActual +1

            long_en_bytes = sys.getsizeof(cantidadDeDocs)

            dicTemporal.setdefault(termId,(posicionInicial,cantidadDeDocs,long_en_bytes))  

            posicionInicial = posicionActual
            cantidadDeDocs=0

        return (dicIntArray,dicTemporal)

# ENCONTRAR PALABRA
def encontrarNoticiasdePalabra(palabras, diccionarioMergeado):

    palabrasSeparadas = palabras.split()
    if not diccionarioMergeado:
        print("No hay diccionario en memoria")
    else:    
        for palabra in palabrasSeparadas:
            
            listaDeNoticiasID = []
            listaDeNoticias = []
            listaDeDiccionarioDocID = recuperarListaDeIndiceDocID()
            listaDeDiccionarioTermID = recuperarListaDeIndiceTermID()
            listaDeDiccionarioDoc = recuperarListaDeIndiceDoc()
            palabraStemmeada = stemmer.stem(palabra.lower())
            for numeroTermID,termino in listaDeDiccionarioTermID.items():
                if termino == palabraStemmeada:         
                    if numeroTermID in diccionarioMergeado:
                        listaDeNoticiasID.append(diccionarioMergeado[numeroTermID])
            if len(listaDeNoticiasID) == 0:
                print(colored("\n---------------------La palabra '"+palabra+"' no se encuentra en ninguna noticia---------------------", 'red'))
            else:
                print(colored("\n ---------------------  Las noticias relacionadas con '"+palabra+"' son:  ---------------------",'green'))
            for arrayNoticiaID in listaDeNoticiasID:
                for noticiaID in arrayNoticiaID:
                    for numeroDocID,noticia in listaDeDiccionarioDocID.items():
                        if noticiaID == numeroDocID:
                            for doc in listaDeDiccionarioDoc:
                                
                                if listaDeDiccionarioDoc[doc] == noticia:
                                    listaDeNoticias.append(doc)
                                    print("\n",doc)

def obtener_docs_ids_con_tupla(tupla):

    lista = []

    for x in range(1,tupla[1]+1):
        lista.append(int_array[tupla[0]+x])

     return lista
