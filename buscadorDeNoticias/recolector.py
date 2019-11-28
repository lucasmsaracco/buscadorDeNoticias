import configparser
import xml.etree.ElementTree as ET
import urllib.request
import urllib
from xml.etree.ElementTree import ElementTree
from xml.etree.ElementTree import Element
import time
import os
import sys

class Recolector:

    def crearCarpetas(self):
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
        print("Se creó exitosamente!")            

     

    def descargarNoticias(self):

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
                        self.texto = self.data.decode('utf-8')
                        self.rootActual = ET.fromstring(self.texto)  
                        self.treeToSave = ET.parse("out/"+diario+"/"+seccion+"/"+seccion+".xml")
                        self.rootToSave = self.treeToSave.getroot()
                    except Exception:
                        print("No se puedo descargar una noticia")

                    for item in self.rootActual[0].findall("item"):

                        self.titulo = item.find("title").text
                        self.pubDate = item.find("pubDate").text

                        if(self.noSeGuardo(self.rootToSave,self.titulo,self.pubDate,"pubDate",seccion)):
                            
                            self.rootToSave.append(item)
                            print("item agregado en DIARIO:",diario,"  SECCION: ",seccion)
                            self.treeToSave.write("out/"+diario+"/"+seccion+"/"+seccion+".xml")
                                
                                                          
    def noSeGuardo(self,root,title,date,datetag,seccion):


        for item in root.findall("item"):

            self.titleItem =item.find("title").text
            self.dateItem =item.find(datetag).text

            if(title == self.titleItem and date == self.dateItem):

                print("item repetido en seccion     ",seccion)
                return False

        return True

    
