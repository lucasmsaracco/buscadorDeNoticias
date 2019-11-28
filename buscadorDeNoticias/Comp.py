import pickle
from bsbi import FuncionesBSBI

class Comp:

    def __init__(self):

        self.bsbi = FuncionesBSBI()
        self.index = self.bsbi.recuperarIndice()
        self.int_array = self.bsbi.recuperarIntArray()
        

    def imprimir(self):
        print(self.int_array)
            

    def comprimir_int_array(self, int_array, index):

        self.new_array = []

        for term_id in index.keys():

            self.doc_ids = self.bsbi.obtenerDocsIdsConTupla(index.get(term_id), int_array) 
            
            self.new_array.append(self.doc_ids[0])
            if(len(self.doc_ids) >1):


                for num in range(0,len(self.doc_ids)-1):
                    
                    self.new_array.append(self.doc_ids[num+1]-self.doc_ids[num])
            
        
        return self.new_array

    def descomprimir_int_array(self,int_array,index):

        self.temp_lista = []

        for term_id in index.keys():

            self.doc_ids = self.descomprimir_lista_de_doc_ids(self.bsbi.obtenerDocsIdsConTupla(index.get(term_id), int_array))

            for doc_id in self.doc_ids:
                self.temp_lista.append(doc_id)

        return self.temp_lista
            
            
       
    
    def obtener_docs_ids_con_tupla(self,tupla):

        self.lista = []
        self.int_array = self.bsbi.recuperarIntArray()
        for x in range(tupla[1]):
            self.lista.append(self.int_array[tupla[0]+x])

        return self.lista

    def descomprimir_lista_de_doc_ids(self,lista):
    
        self.temp = []

        self.temp.append(lista[0])
        
        for num in range(len(lista)-1):

           

            self.temp.append(lista[num+1]+self.temp[num])


        return self.temp
            

# x = FuncionesBSBI()
# w = x.recuperarIndice()
# z = x.recuperarIntArray()
# y = Comp()
# print(y.comprimir_int_array(z,w))         
            



##pepe =Comp()
##pepe.cargar_datos()
####pepe.imprimir()
##
##lista_comprimida = pepe.comprimir_int_array(pepe.int_array,pepe.index)
##
##print(pepe.descomprimir_int_array(lista_comprimida,pepe.index))
