# from bitarray import bitarray
# import sys

# numeroBinarioPython = bin(254).replace("0b","")
# numeroBinarioBitarray = bitarray()

# for numero in numeroBinarioPython:
#     numeroTemporal = int(numero)
#     if numeroTemporal == 1:
#         numeroBinarioBitarray.append(True)
#     if numeroTemporal == 0:
#         numeroBinarioBitarray.append(False) 
# while(True):
#     if len(numeroBinarioBitarray) <=7:
#         numeroBinarioBitarray.insert(0,0)
#     else:
#         break


# print(numeroBinarioBitarray)

# print(sys.getsizeof(numeroBinarioBitarray), sys.getsizeof(numeroBinarioPython))

class tumama:

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

#a es 7, b es 128 c es 2
a = [1,0,0,0,0,1,1,1]
b = [0,0,0,0,0,0,0,1,1,0,0,0,0,0,0,0]
c= [1,0,0,0,0,0,1,0]
lista = a+b+c

x = tumama()
pepe = x.obtener_numeros_binarios_desde_lista_de_binarios_en_fila(lista)
print(pepe)