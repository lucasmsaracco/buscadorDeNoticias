from UncompressedPostings import UncompressedPostings
import array
test = UncompressedPostings()

# COMPRIMIR EN BYTEARRAY UNA LISTA DE ENTEROS
def compresionDeListaDeEnteros(lista):

    resultado = array.array("L",lista).tobytes()
    decode = array.array("L")
    decode.frombytes(resultado)
    hola = decode.tolist()
    return hola

print(compresionDeListaDeEnteros([141, 20, 60]))