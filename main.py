import configparser
import xml.etree.ElementTree as ET
import urllib.request
import urllib
from xml.etree.ElementTree import ElementTree
from xml.etree.ElementTree import Element

ig = configparser.ConfigParser()
archivo = ig.read("config.ini")
secciones = ig.sections()
print(secciones)