from nltk.corpus import stopwords
from nltk.stem import SnowballStemmer
import nltk
import re
diccionarioDeTextos = {"texto1": "Cojer cojio cojia", "texto2": "Un texto es una composición de signos codificados en un sistema de escritura que forma una unidad de sentido. También es una composición de caracteres imprimibles generados por un algoritmo de cifrado que, aunque no tienen sentido para cualquier persona, sí puede ser descifrado por su destinatario original",
                       "texto3": "Con origen en el latín textus, la palabra texto describe a un conjunto de enunciados que permite dar un mensaje coherente y ordenado, ya sea de manera escrita o a través de la palabra. Se trata de una estructura compuesta por signos y una escritura determinada que da espacio a una unidad con sentido."}
stemmer = SnowballStemmer("spanish")
palabras_minuscula = []
palabras_stemmeadas = []
dicInv = {}

def stemmear():
    for key in diccionarioDeTextos:
        palabras = re.findall(r"\w+", diccionarioDeTextos[key])
        
        for palabra in palabras:
            palabras_minuscula.append(palabra.lower())
    filtered_words = [
        word for word in palabras_minuscula if word not in stopwords.words('spanish')]
        
    for word in filtered_words:
        if stemmer.stem(word) in palabras_stemmeadas:
            pass
        else:
            palabras_stemmeadas.append(stemmer.stem(word))

    return palabras_stemmeadas

def invertirDiccionario(palabras_stemmeadas):
    
    for key in diccionarioDeTextos:
        for palabra in palabras_stemmeadas: 
            if palabra in diccionarioDeTextos[key]:
                if palabra not in dicInv.keys():
                    dicInv[palabra]=[key]
                else:
                    dicInv[palabra].append(key)

    print(dicInv)

stemmear()
     
