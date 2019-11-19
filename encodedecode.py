from UncompressedPostings import UncompressedPostings

class EncodeDecode:

        # ENCODEA DICCIONARIO INVERTIDO
    def encodearDocs(self,dicInv):
        self.dicNuevo={}
        for key in dicInv:
            self.byteArray = UncompressedPostings.encode(dicInv[key])
            self.dicNuevo[key] = self.byteArray 
        return self.dicNuevo  

    # DECODEA DICCIONARIO ENCODEADO
    def decodearDocs(self,dicInvEncodeado):
        self.dicNuevo={}
        for key in dicInvEncodeado: 
            self.value = UncompressedPostings.decode(dicInvEncodeado[key])
            self.dicNuevo[key]=self.value
        return self.dicNuevo    