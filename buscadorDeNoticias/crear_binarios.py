import pickle

import bsbi
from bitarray import bitarray

class Bit_array:

    def dividir_numero(self,numero):

    ##        print("Numero en decimal",numero)

            self.primer_byte = []
            self.segundo_byte = []
            self.tercer_byte = []
            self.cuarto_byte = []
            self.un_byte =[]
            self.binario = bin(numero)[2:]
    ##        print("Numero en binario",self.binario)
            ##OCUPA 1 BYTE/ EL NUMERO BINARIO TIENE 7 DIGITOS ( 7 BITS) + UN BIT QUE SE AGREGA AL PRINCIPIO (1) PARA INDICAR QUE TERMINA
            if numero < 128:


                for bit in self.binario:
                    self.un_byte.append(int(bit))

                for bit in range(8-len(self.binario)-1):
                    self.un_byte.insert(0,0)


                self.un_byte.insert(0,1)

                return self.un_byte

            ##OCUPA 2 BYTE

            if numero>=128 and numero<16384:

                ##Primer Byte

                for bit in range(len(self.binario)-7):

                    self.primer_byte.append(int(self.binario[bit]))

                for num in range(8-((len(self.binario)-7))):

                    self.primer_byte.insert(0,0)

                ##Segundo Byte

                for bit in range(len(self.binario)-7,len(self.binario)):
                    self.segundo_byte.append(int(self.binario[bit]))


                self.segundo_byte.insert(0,1)
                return self.primer_byte+self.segundo_byte

            #OCUPA 3 BYTES ### num >= 2**21 a partir de ese 4 bytes
            if numero>= 16384 and numero < 2097152:

                ###Primer Byte



                for bit in range(len(self.binario)-14):

                    self.primer_byte.append(int(self.binario[bit]))

                for num in range(8-((len(self.binario)-14))):

                    self.primer_byte.insert(0,0)

                ###Segundo Byte
                for bit in range(len(self.binario)-14,len(self.binario)-7):
                    self.segundo_byte.append(int(self.binario[bit]))


                self.segundo_byte.insert(0,0)

                ###Tercer Byte
                for bit in range((len(self.binario)-7),len(self.binario)):
            ##      for bit in range((len(binario)-14)+7,len(binario)):
                    self.tercer_byte.append(int(self.binario[bit]))

                self.tercer_byte.insert(0,1)

                return self.primer_byte + self.segundo_byte + self.tercer_byte

            ##OCUPA 4 BYTES

            if numero >= 2097152 and numero < 268435456:

                ###Primer Byte

                for bit in range(len(self.binario)-21):

                    self.primer_byte.append(int(self.binario[bit]))

                for num in range(8-((len(self.binario)-21))):

                    self.primer_byte.insert(0,0)

                ###Segundo Byte
                for bit in range(len(self.binario)-21,len(self.binario)-14):
                    self.segundo_byte.append(int(self.binario[bit]))


                self.segundo_byte.insert(0,0)

                ###Tercer Byte
                for bit in range((len(self.binario)-14),len(self.binario)-7):
                    self.tercer_byte.append(int(self.binario[bit]))

                self.tercer_byte.insert(0,0)

                ##Cuarto Byte

                for bit in range((len(self.binario)-7),len(self.binario)):
                    self.cuarto_byte.insert(0,1)
                self.cuarto_byte.insert(0,1)

                return self.primer_byte + self.segundo_byte + self.tercer_byte + self.cuarto_byte


    #   ESTE METODO RECIBE EL INT ARRAY CON LOS SALTOS ENTRE DOC_IDS Y EL INDICE TERM_ID TUPLA
    # UTILIZA EL INT_ARRAY, CREA UN INT_ARRAY COMPRIMIDO CON LOS SALTOS ENTRE DOC_IDS
    # LUEGO CREA EL ARREGLO DE BINARIOS

    def crear_arreglo_de_binarios(self,int_array,index):
        

        self.arreglo_binario = []

        for numero in int_array:

            for bit in self.dividir_numero(numero):
                self.arreglo_binario.append(bit)

        return self.arreglo_binario

    def comprimir_lista_de_apariciones_en_bitarray(self, arregloBinario):

        numeroBinarioBitarray = bitarray()

        for numero in arregloBinario:
            if numero == 1:
                numeroBinarioBitarray.append(True)
            if numero == 0:
                numeroBinarioBitarray.append(False)

        with open("bit_array.pickle","wb") as archivo:
            pickle.dump(numeroBinarioBitarray,archivo)

        





    def obtener_numeros_binarios_desde_lista_de_binarios_en_fila(self,lista_de_numeros_en_binario):

        ##SACAR TAJOS DE BYTES
        self.temp=[]
        self.byteIniciaCon0 =False
        self.byteIniciaCon1 = False
        self.contador = 0
        self.lista_salida = []


        self.pos = 8
        for num in range(len(lista_de_numeros_en_binario)):

            if(num % self.pos == 0):
                if(lista_de_numeros_en_binario[num]==0):
                     self.byteIniciaCon0=True

                if(lista_de_numeros_en_binario[num]==1):
                     self.byteIniciaCon1=True


            if(self.byteIniciaCon0 and self.contador<self.pos):
                 self.temp.append(lista_de_numeros_en_binario[num])
                 self.contador =  self.contador +1
            #CUANDO TERMINE ESTO, TERMINA
            if( self.byteIniciaCon1 and  self.contador<self.pos):
                 self.temp.append(lista_de_numeros_en_binario[num])
                 self.contador =  self.contador+1

            if( self.contador == self.pos and  self.byteIniciaCon1):
                 self.lista_salida.append(self.temp)


                 self.temp = []

        ##SI EL TEMP TIENE YA UNO O VARIOS BYTES, SE DEBE SETEAR QUE DEBE BUSCAR OTRO BYTE
            if(len(self.temp)%self.pos == 0):
                self.byteIniciaCon0 = False
                self.byteIniciaCon1 = False
                self.contador = 0


        return self.lista_salida



        #A ESTE METODO
    def decodificar_lista(self,lista):

        ###DECODIFICAR NORMALIZAR BINARIOS
        self.lista_de_decimales = []
        for numero in lista:

            if(len(numero)==8):
                #saco el 1 del principio
                numero[0]=0
                decimal_actual = ""
                for x in numero:
                    decimal_actual = decimal_actual + str (x)

                self.lista_de_decimales.append(int(decimal_actual,2))

            if(len(numero)==16):
                decimal_actual = ""
                for i in range(0,16):
                    if i != 8:
                        decimal_actual = decimal_actual + str(numero[i])

                self.lista_de_decimales.append(int(decimal_actual,2))

            if len(numero)==24:
                decimal_actual = ""
                for i in range(0,24):
                    if i != 8 and i != 16:
                        decimal_actual = decimal_actual + str(numero[i])

                self.lista_de_decimales.append(int(decimal_actual,2))

            if len(numero)==32:
                decimal_actual = ""
                for i in range(0,32):
                    if i != 8 and i != 16 and i != 24:
                        decimal_actual = decimal_actual + str(numero[i])

                self.lista_de_decimales.append(int(decimal_actual,2))

        return self.lista_de_decimales


    def ejecutar_compresion_y_guardar_en_disco(self,int_array,index):


        ##COMPRESOR COMPRIME LOS SALTOS ENTRE DOC_ID
        self.int_array_comprimido = bsbi.FuncionesBSBI().comprimir_int_array(int_array,index)


        self.bit_array = Bit_array()


        # Creo el arreglo binario
        self.arreglo_de_binarios = self.bit_array.crear_arreglo_de_binarios(self.int_array_comprimido,index)


        # comprimo en bytearray y lo guardo en disco
        self.bit_array.comprimir_lista_de_apariciones_en_bitarray(self.arreglo_de_binarios)
        

# w=FuncionesBSBI()
# z=w.recuperarIndice()
# y=w.recuperarIntArray()
# x = Bit_array()
# x.ejecutar_compresion_y_guardar_en_disco(y,z)     

    def obtener_tajadas_binarias_de_int_array_comprimido(self):
        
        self.int_array_comprimido = []
        #CARGO EN MEMORIA EL BIT_ARRAY
        with open("bit_array.pickle","rb") as archivo:
            self.int_array_comprimido= pickle.load(archivo)

        self.int_array_descomprimido = []

        for x in self.int_array_comprimido:
            if(x == True):
                self.int_array_descomprimido.append(1)
            else:
                self.int_array_descomprimido.append(0)
        
        
        return self.obtener_numeros_binarios_desde_lista_de_binarios_en_fila(self.int_array_descomprimido)

    def obtener_doc_ids(self,lista,tupla):

        self.out = []
        
        for x in range(tupla[1]):
            self.out.append(lista[tupla[0]+x])    
        
        self.lista_de_doc_ids = self.decodificar_lista(self.out)
        

        return self.lista_de_doc_ids





































