import xml.etree.ElementTree as ET
import configparser
import os
from nltk.corpus import stopwords
from nltk.stem import SnowballStemmer
import nltk
import re
import pickle
import collections
import array
import sys
from termcolor import colored
from encodedecode import EncodeDecode
import crear_binarios



class FuncionesBSBI:


    def __init__(self):

        self.ig = configparser.ConfigParser()
        self.archivo = self.ig.read("config.ini")
        self.diarios = self.ig.sections()
        self.stemmer = SnowballStemmer("spanish")
        self.descripcion = []
        self.ultimoDocID = 0
        self.ultimoTermID = 0
        self.encodedecode = EncodeDecode()

    # GENERA DICCIONARIO DOCID->DOC A PARTIR DE DICCIONARIO DE DOC->STRING(TERMINOS)
    def construirDocID(self,diccionarioDeDocs):
        diccionarioTemporal={}
        self.ultimoDocID
        self.x=0
        values = list(diccionarioDeDocs.values()) 
        for i in range(1 + self.ultimoDocID,len(diccionarioDeDocs.keys())+self.ultimoDocID+1):
            diccionarioTemporal[i]=values[self.x]
            self.x=self.x+1
        self.ultimoDocID=self.ultimoDocID+len(diccionarioDeDocs.keys())
        return diccionarioTemporal


    # GENERA DICCIONARIO TERMID->TERM A PARTIR DE LISTA DE PALABRAS STEMMEADAS
    def construirTermID(self,palabras_stemmeadas):
        diccionarioTemporal={}
        self.ultimoTermID
        self.x=0
        for i in range(1 + self.ultimoTermID,len(palabras_stemmeadas)+self.ultimoTermID+1):
            if palabras_stemmeadas[self.x] in list(diccionarioTemporal.values()):
                pass
            else:
                diccionarioTemporal[i]=palabras_stemmeadas[self.x]
            self.x=self.x+1
        self.ultimoTermID=self.ultimoTermID+len(palabras_stemmeadas)
        return diccionarioTemporal    


    # DEVUELVE DICCIONARIO DE DOCUMENTO -> STRING(TERMINOS)
    def parsear_bloque(self,num):
        
        self.diccionarioDeDocs={}
        for seccion in self.ig[self.diarios[num]]:
            if seccion != "query_interval" and seccion != "tmp" and seccion != "output" and seccion != "url_base":
                self.tree = ET.parse('out/'+self.diarios[num]+'/'+seccion+'/'+seccion+'.xml')
                self.root = self.tree.getroot()
                for item in self.root.findall("item"):
                    self.descripcionTemporal=item.find('description')
                    if self.descripcionTemporal != None:
                        if self.descripcionTemporal.text != None:
                            if item.find("title").text+ " " +item.find("description").text in self.diccionarioDeDocs.values():
                                pass
                            else:
                                self.diccionarioDeDocs[self.diarios[num]+"-"+seccion+"-"+item.find("title").text+"-"+item.find("pubDate").text]=item.find("title").text+ " " +item.find("description").text
        return(self.diccionarioDeDocs)

    # DEVUELVE LISTA DE PALABRAS STEMMEADAS EN EL DICCIONARIO DOCUMENTO -> STRING(TERMINOS)
    def stemmear(self,diccionarioDeID):
        self.palabras_minuscula = []
        self.palabras_stemmeadas = []
        for key in diccionarioDeID:
            self.palabras = re.findall(r"[A-z]+[áéíóú]?[A-z]*", diccionarioDeID[key].lower())
        
            for palabra in self.palabras:
                self.palabras_minuscula.append(palabra)
        self.filtered_words = [word for word in self.palabras_minuscula if word not in stopwords.words('spanish') and not len(word) < 4]
        
        for word in self.filtered_words:
            if self.stemmer.stem(word) in self.palabras_stemmeadas:
                pass
            else:
                self.palabras_stemmeadas.append(self.stemmer.stem(word))  
        return(self.palabras_stemmeadas)


    #GENERA DICCIONARIO TERMID->DOCID
    def invertirDiccionario(self, diccionarioDeTermID, diccionarioDeDocID):

        self.dicInv={}
        for key in diccionarioDeDocID:
            self.texto = self.stemmer.stem(diccionarioDeDocID[key].replace('"',"").lower())
            for numeroPalabra in diccionarioDeTermID:
                if diccionarioDeTermID[numeroPalabra] in self.texto:
                    if numeroPalabra not in self.dicInv.keys():
                        self.dicInv[numeroPalabra]=[key]
                    else:
                        if key not in self.dicInv[numeroPalabra]:             
                            self.dicInv[numeroPalabra].append(key)
        return(self.dicInv)

    #MERGEA DICICONARIO TERMID->DOCID

    def mergearListaDeDiccionarios(self,diccionarioCompleto, dicTermID):
        self.diccionarioDePrueba = {}
        self.diccionarioNuevo = {}
        for key,value in dicTermID.items():
            if value not in self.diccionarioDePrueba:
                self.diccionarioDePrueba[value] = [key]
            else:
                self.diccionarioDePrueba[value].append(key)
        for key in self.diccionarioDePrueba:
            self.suma = []
            if len(self.diccionarioDePrueba[key]) > 1:
                for position in self.diccionarioDePrueba[key]:
                    if position in diccionarioCompleto.keys():
                        self.suma = self.suma + diccionarioCompleto[position]
                if len(self.suma)!=0:        
                    self.diccionarioNuevo[self.diccionarioDePrueba[key][0]] = self.suma
            else:
                if self.diccionarioDePrueba[key][0] in diccionarioCompleto.keys():
                    self.diccionarioNuevo[self.diccionarioDePrueba[key][0]]= diccionarioCompleto[self.diccionarioDePrueba[key][0]]                
        return(self.diccionarioNuevo)    

    

            


    # GUARDA DICCIONARIOS TERMID->TERM CON PICKLE
    def guardarListaDeIndiceTermID(self,listaDeIndiceTermID):
        with open("out/diccionario_termid-term.pickle","wb") as handle:
            pickle.dump(listaDeIndiceTermID, handle, protocol=pickle.HIGHEST_PROTOCOL)    


    # GUARDA DICCIONARIOS DOCID->STRING CON PICKLE
    def guardarListaDeIndiceDocID(self,listaDeIndiceDocID):
        with open("out/diccionario_docid-doc.pickle","wb") as handle:
            pickle.dump(listaDeIndiceDocID, handle, protocol=pickle.HIGHEST_PROTOCOL)

    # GUARDA INDICE INVERTIDO CON PICKLE
    def guardarIndiceInvertido(self,diccionarioAGuardar):
        for i in range(0,len(self.diarios)):
            with open("out/"+self.diarios[i]+"/"+"diccionario_"+self.diarios[i]+".pickle","wb") as handle:
                pickle.dump(self.encodedecode.encodearDocs(diccionarioAGuardar[i]), handle, protocol=pickle.HIGHEST_PROTOCOL)        

    # GUARDA DICCIONARIOS DOC->STRING CON PICKLE
    def guardarListaDeIndiceDoc(self,listaDeIndiceDocID):
        with open("out/diccionario_doc-terms.pickle","wb") as handle:
            pickle.dump(listaDeIndiceDocID, handle, protocol=pickle.HIGHEST_PROTOCOL)

    # GUARDA LISTA DE INTARRAY
    def guardarIntArray(self, listaIntArray):
        with open("out/intArray.pickle","wb") as handle:
            pickle.dump(listaIntArray, handle, protocol=pickle.HIGHEST_PROTOCOL)                    

    # RECUPERA DICICONARIO TERMID->DOCID CON PICKLE, LO MERGEA, Y LO TRANSFORMA A TERMID->TUPLA PARA USARLO EN MEMORIA
    def recuperarIndice(self):
        self.b=[]
        self.temp = {}
        self.index = {}
        for i in range(0, len(self.diarios)):
            with open("out/"+self.diarios[i]+"/"+"diccionario_"+self.diarios[i]+".pickle", 'rb') as handle:
                self.b.append(self.encodedecode.decodearDocs(pickle.load(handle)))   
        for diccionario in self.b:
            for termid in diccionario:
                self.temp[termid] = diccionario[termid]
        self.index = self.generarIntArray_y_DicConTupla(self.mergearListaDeDiccionarios(self.temp, self.recuperarListaDeIndiceTermID()))[1]        
        return self.index      

    # RECUPERA DICICONARIO DOCID->DOC CON PICKLE
    def recuperarListaDeIndiceDocID(self):
        with open("out/diccionario_docid-doc.pickle", 'rb') as handle:
            return pickle.load(handle)

    # RECUPERA DICICONARIO DOC->STRING CON PICKLE
    def recuperarListaDeIndiceDoc(self):
        with open("out/diccionario_doc-terms.pickle", 'rb') as handle:
            return pickle.load(handle)            

    # RECUPERA DICICONARIO TERMID->TERM CON PICKLE
    def recuperarListaDeIndiceTermID(self):
        with open("out/diccionario_termid-term.pickle", 'rb') as handle:
            return pickle.load(handle)
    
    # RECUPERA LISTA DE INTARRAY
    def recuperarIntArray(self):
        with open("out/intArray.pickle", 'rb') as handle:
            return pickle.load(handle)


    # ARCHIVO MAIN
    def mainIndiceInvertido(self):
        self.diccionario = {}
        self.lista = []
        self.diccionarioNuevoDocID = {}
        self.diccionarioNuevoTermID = {}
        self.diccionarioDocTerm = {}
        self.newDict = {}
        self.temp = 0
        self.intArray = []
        self.finalDict= {}
        # iteraciones sobre todos los bloques
        for i in range(0,len(self.diarios)):
            # SE PRINTEA PARA CHECKEAR QUE BLOQUE SE ESTA INVIRTIENDO
            print(self.diarios[i])
            self.bloqueParseado = self.parsear_bloque(i)
            # ALMACENA TODOS LOS DOC->NOTICIA
            for key in self.bloqueParseado:
                self.diccionarioDocTerm[key] = self.bloqueParseado[key]
            self.diccionarioDocID = self.construirDocID(self.bloqueParseado)
            # ALMACENA TODOS LOS DOCID->NOTICIA
            for key in self.diccionarioDocID:
                self.diccionarioNuevoDocID[key]=self.diccionarioDocID[key]
            self.diccionarioTermID =self.construirTermID(self.stemmear(self.diccionarioDocID))
            # ALMACENA TODOS LOS TERMID->TERM
            for key in self.diccionarioTermID:
                self.diccionarioNuevoTermID[key]=self.diccionarioTermID[key]
            self.diccionarioTemporal=self.invertirDiccionario(self.diccionarioTermID, self.diccionarioDocID)
            # AGREGA DICCIONARIO TERMID->DOCID DE CADA BLOQUE A LA LISTA A FIN DE SER GUARDADOS TODOS JUNTOS EN CADA BLOQUE EN ESPECIFICO 
            self.lista.append(self.diccionarioTemporal)
            # AGREGA SE MERGEA CONSTANTEMENTE LOS DICCIONARIOS TERMID->DOCID DE TODOS LOS BLOQUES A UN DICCIONARIO GLOBAL
            for key in self.diccionarioTemporal:
                self.diccionario[key]=self.diccionarioTemporal[key]
            # SE PRINTEA PARA CHECKEAR EL CORRECTO FUNCIONAMIENTO DEL DICCIONARIO TERMID->DOCID   
            print(self.diccionarioTemporal)
        # MERGEA EL DICCIONARIO TERMID->DOCID    
        self.newDict=self.mergearListaDeDiccionarios(dict(collections.OrderedDict(sorted(self.diccionario.items()))),self.diccionarioNuevoTermID)
        # LUEGO DE MERGEAR SE OBTIENE LA TUPLA CON EL INTARRAY Y EL DICCIONARIO TERMID->TUPLE
        self.temp = self.generarIntArray_y_DicConTupla(self.newDict)
        # SE ASIGNA EL INTARRAY
        self.intArray = self.temp[0]
        # SE ASIGNA EL DICCIONARIO TERMID->TUPLE FINAL
        self.finalDict = self.temp[1]
        # GUARDA INTARRAY PARA COMODIDAD POSTERIOR
        self.guardarIntArray(self.intArray)
        # GUARDA DICCIONARIO DOC->NOTICIA PARA COMODIDAD POSTERIOR
        self.guardarListaDeIndiceDoc(self.diccionarioDocTerm)
        # GUARDA DICCIONARIO DOCID->NOTICIA PARA COMODIDAD POSTERIOR
        self.guardarListaDeIndiceDocID(self.diccionarioNuevoDocID)
        # GUARDA DICCIONARIO TERMID->TERM PARA COMODIDAD POSTERIOR
        self.guardarListaDeIndiceTermID(self.diccionarioNuevoTermID)
        self.guardarIndiceInvertido(self.lista)
        return (self.finalDict, self.lista)    

# METODO QUE CONVIERTE EL DICCIONARIO TERMID-DOCID
    def generarIntArray_y_DicConTupla(self,dic):

            self.dicTemporal = {}
            self.dicIntArray = []
            self.posicionInicial = 0
            self.cantidadDeDocs = 0
            self.posicionActual = 0

            for termId in dic.keys():

                for docId in dic.get(termId):

                    self.dicIntArray.append(docId)

                    self.cantidadDeDocs = self.cantidadDeDocs + 1
                    self.posicionActual = self.posicionActual + 1

                self.long_en_bytes = sys.getsizeof(self.cantidadDeDocs)

                self.dicTemporal.setdefault(termId,(self.posicionInicial,self.cantidadDeDocs,self.long_en_bytes))  

                self.posicionInicial = self.posicionActual
                self.cantidadDeDocs=0

            return (self.dicIntArray,self.dicTemporal)

    # ENCONTRAR PALABRA
    def encontrarNoticiasdePalabra(self,palabras, diccionarioMergeado, intArray):

        self.palabrasSeparadas = palabras.split()
        if not diccionarioMergeado:
            print(colored("No hay diccionario en memoria", "red"))
        else:    
            for palabra in self.palabrasSeparadas:
                self.listaDeNoticiasID = []
                self.listaDeNoticias = []
                self.listaDeDiccionarioDocID = self.recuperarListaDeIndiceDocID()
                self.listaDeDiccionarioTermID = self.recuperarListaDeIndiceTermID()
                self.listaDeDiccionarioDoc = self.recuperarListaDeIndiceDoc()
                self.palabraStemmeada = self.stemmer.stem(palabra.lower())
                self.intArrayTemp = intArray 
                for numeroTermID,termino in self.listaDeDiccionarioTermID.items():
                    if termino == self.palabraStemmeada:         
                        if numeroTermID in diccionarioMergeado:
                                self.listaDeNoticiasID.append(self.obtenerDocsIdsConTupla(diccionarioMergeado[numeroTermID],self.intArrayTemp))

                if len(self.listaDeNoticiasID) == 0:
                    print(colored("\n---------------------La palabra '"+palabra+"' no se encuentra en ninguna noticia---------------------", 'red'))
                else:
                    print(colored("\n ---------------------  Las noticias relacionadas con '"+palabra+"' son:  ---------------------",'green'))
                for arrayNoticiaID in self.listaDeNoticiasID:
                    for noticiaID in arrayNoticiaID:
                        for numeroDocID,noticia in self.listaDeDiccionarioDocID.items():
                            if noticiaID == numeroDocID:
                                for doc in self.listaDeDiccionarioDoc:
                                    
                                    if self.listaDeDiccionarioDoc[doc] == noticia:
                                        self.listaDeNoticias.append(doc)
                                        print("\n",doc)

    # ENCONTRAR PALABRA
    def encontrarNoticiasdePalabraComprimida(self,palabras, diccionarioMergeado, lista):

        self.palabrasSeparadas = palabras.split()
        if not diccionarioMergeado:
            print(colored("No hay diccionario en memoria", "red"))
        else:    
            for palabra in self.palabrasSeparadas:
                self.listaDeNoticiasID = []
                self.listaDeNoticias = []
                self.listaDeDiccionarioDocID = self.recuperarListaDeIndiceDocID()
                self.listaDeDiccionarioTermID = self.recuperarListaDeIndiceTermID()
                self.listaDeDiccionarioDoc = self.recuperarListaDeIndiceDoc()
                self.palabraStemmeada = self.stemmer.stem(palabra.lower())
                for numeroTermID,termino in self.listaDeDiccionarioTermID.items():
                    if termino == self.palabraStemmeada:         
                        if numeroTermID in diccionarioMergeado:
                                self.listaDeNoticiasID.append(crear_binarios.Bit_array().obtener_doc_ids(lista, diccionarioMergeado[numeroTermID]))

                if len(self.listaDeNoticiasID) == 0:
                    print(colored("\n---------------------La palabra '"+palabra+"' no se encuentra en ninguna noticia---------------------", 'red'))
                else:
                    print(colored("\n ---------------------  Las noticias relacionadas con '"+palabra+"' son:  ---------------------",'green'))
                for arrayNoticiaID in self.listaDeNoticiasID:
                    for noticiaID in arrayNoticiaID:
                        for numeroDocID,noticia in self.listaDeDiccionarioDocID.items():
                            if noticiaID == numeroDocID:
                                for doc in self.listaDeDiccionarioDoc:
                                    
                                    if self.listaDeDiccionarioDoc[doc] == noticia:
                                        self.listaDeNoticias.append(doc)
                                        print("\n",doc)
   

    def obtenerDocsIdsConTupla(self,tupla, intArray):
        
        self.lista = []
        
        for x in range(tupla[1]):
            self.lista.append(intArray[tupla[0]+x])    
      
        return(self.lista)

    def comprimir_int_array(self, int_array, index):

        self.new_array = []

        for term_id in index.keys():

            self.doc_ids = self.obtenerDocsIdsConTupla(index.get(term_id), int_array) 
            
            self.new_array.append(self.doc_ids[0])
            if(len(self.doc_ids) >1):


                for num in range(0,len(self.doc_ids)-1):
                    
                    self.new_array.append(self.doc_ids[num+1]-self.doc_ids[num])
            
        
        return self.new_array

    def descomprimir_int_array(self,int_array,index):

        self.temp_lista = []

        for term_id in index.keys():

            self.doc_ids = self.descomprimir_lista_de_doc_ids(self.obtenerDocsIdsConTupla(index.get(term_id), int_array))

            for doc_id in self.doc_ids:
                self.temp_lista.append(doc_id)

        return self.temp_lista

    def descomprimir_lista_de_doc_ids(self,lista):
    
        self.temp = []

        self.temp.append(lista[0])
        
        for num in range(len(lista)-1):

           

            self.temp.append(lista[num+1]+self.temp[num])


        return self.temp