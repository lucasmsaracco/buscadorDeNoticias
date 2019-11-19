from UncompressedPostings import UncompressedPostings

class Compresion():
    
    @staticmethod
    def comprimir(intArray, dicInvertido):
        byteArray = UncompressedPostings.encode(intArray)
        i = 0
        while i < len(intArray):

            termID = intArray[i]
            documentos = dicInvertido[termID][1]
            byteArray.append(termID)
            byteArray.append(intArray[i + 1])

            if documentos > 1:

                for j in range(0, documentos - 1):

                    n = abs(intArray[i + j + 1] - intArray[i + j + 1 + 1])

                    if n < 128:
                        n = Compresion.setBit(n, 7)
                    elif n < 32768:
                        n = Compresion.setBit(n, 15)
                    else:
                        n = Compresion.setBit(n, 31)

                    byteArray.append(n)

            i = i + documentos + 1

        return byteArray

    @staticmethod
    def setBit(int_type, offset):
        mask = 1 << offset
        return(int_type | mask)