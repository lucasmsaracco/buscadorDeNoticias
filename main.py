import configparser
import xml.etree.ElementTree as ET
import urllib.request
import urllib
from xml.etree.ElementTree import ElementTree
from xml.etree.ElementTree import Element
import time
import os
import sys

class Main:

    def crear_arboles_de_salida(self):
        self.ig = configparser.ConfigParser()
        self.archivo = self.ig.read("config.ini")
        self.diarios = self.ig.sections()
        for diario in self.diarios:
            os.mkdir("out/"+diario)
            
            for seccion in self.ig[diario]:
                if seccion != "query_interval" and seccion != "tmp" and seccion != "output" and seccion != "url_base":

                    os.mkdir("out/"+diario+"/"+seccion)
                    self.root = Element(seccion)
                    self.tree = ElementTree(self.root)
                    self.tree.write("out/"+diario+"/"+seccion+"/"+seccion+".xml")
        print("Se ha creado con exito")            

     

    def descargar_noticias(self):

        self.ig = configparser.ConfigParser()
        self.archivo = self.ig.read("config.ini")
        self.diarios = self.ig.sections()

        for diario in self.diarios:
            for seccion in self.ig[diario]:
                if seccion != "query_interval" and seccion != "tmp" and seccion != "output" and seccion != "url_base":

                    try:
                        print(diario)
                        print(seccion)
                        self.url_final =self.ig[diario].get(seccion)  
                        self.url_base = self.ig[diario].get("url_base")
                        self.link = self.url_base + self.url_final

                        print(self.link)
                    
                        self.response = urllib.request.urlopen(self.link)
                        self.data = self.response.read()     
                        self.text = self.data.decode('utf-8')
                        
                        self.root_pagina_actual = ET.fromstring(self.text)
                        
                        self.tree_a_guardar = ET.parse("out/"+diario+"/"+seccion+"/"+seccion+".xml")
                        self.root_a_guardar = self.tree_a_guardar.getroot()

                        

                    except Exception:
                        print("una noticia no pudo ser descargada, debido a un error en la decodificacion")
                    if(diario == "DIARIO_DE_IZQUIERDA"):
                        for item in self.root_pagina_actual[0].findall("item"):

                            self.titulo = item.find("title").text
                            self.pubDate = item.find("{http://purl.org/dc/elements/1.1/}date").text


                            if(self.no_fue_guardado(self.root_a_guardar,self.titulo,self.pubDate,"{http://purl.org/dc/elements/1.1/}date",seccion)):

                                self.root_a_guardar.append(item)
                                print("item agregado en DIARIO:",diario,"  SECCION: ",seccion)
                                self.tree_a_guardar.write("out/"+diario+"/"+seccion+"/"+seccion+".xml")
                                
                    else:
                        for item in self.root_pagina_actual[0].findall("item"):

                            self.titulo = item.find("title").text
                            self.pubDate = item.find("pubDate").text

                            if(self.no_fue_guardado(self.root_a_guardar,self.titulo,self.pubDate,"pubDate",seccion)):

                                self.root_a_guardar.append(item)
                                print("item agregado en DIARIO:",diario,"  SECCION: ",seccion)
                                self.tree_a_guardar.write("out/"+diario+"/"+seccion+"/"+seccion+".xml")
                                
                                


##SE INGRESA PRIMERO EL ARBOL YA GUARDADO EN DISCO, LUEGO TITULO Y FECHA A COMPROBAR, LUEGO COMO SE
##LLAMA EL SUBELEMENT QUE CORRESPONDE A LA FECHA EN EL ITEM DEL ARCHIVO GUARDADO                            
    def no_fue_guardado(self,root_a_guardar,titulo,pubDate,tag_fecha,seccion):


        for item_guardado in root_a_guardar.findall("item"):

            self.titulo_item_guardado =item_guardado.find("title").text
            self.pubDate_item_guardado =item_guardado.find(tag_fecha).text

            if(titulo == self.titulo_item_guardado and pubDate == self.pubDate_item_guardado):
                print("item repetido en seccion     ",seccion)
                return False

        return True

    
