class verga:
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


pepe = verga()
print(pepe.dividir_numero(18530))