import msvcrt
import os
from main import Main
import bsbi

class Menu:

    main = Main()
    ans=True
    index = {}
    lista = []
    while ans:
        os.system("cls")
        print ("""
        1.Recolectar noticias
        2.Crear indice invertido
        3.Comrpimir lista de apariciones
        4.Realizar busquedas
        5.Salir del programa
        """)

        print("Ingrese la opcion deseada:")
        ans=msvcrt.getch()

        if ans==b"1": 
            os.system('cls')
            print("Si desea volver atras presione la tecla Esc, si esta seguro de querer recolectar noticias presione ENTER")
            key = None
            while key != b'\x1b' and key != b'\r':
                key = msvcrt.getch()
            if key == b'\x1b':
                pass
            else:
                os.system("cls")
                main.descargar_noticias()

        elif ans==b"2":
            os.system('cls')
            print("Si desea volver atras presione la tecla Esc, si esta seguro de querer acceder al menu de Indices Invertidos presione ENTER")
            key = None
            while key != b'\x1b' and key != b'\r':
                key = msvcrt.getch()
            if key == b'\x1b':
                pass
            else:

                ans2=True
                while(ans2):

                    os.system("cls")
                    print ("""
                    1.Crear indice desde directorio
                    2.Guardar indice en disco
                    3.Cargar indice previamente salvado
                    4.Volver atras
                    """)

                    print("Ingrese la opcion deseada:")
                    ans2=msvcrt.getch()

                    if ans2 ==b"1":
                        temp = bsbi.mainIndiceInvertido()
                        index = temp[0]
                        lista = temp[1]
                        print("Indice creado, aprete ENTER para avanzar")
                        key2 = None
                        while key2 != b'\r':
                            key2 = msvcrt.getch()
                        if key2 == b'\r':
                            pass
                    elif ans2 == b"2":
                        if len(lista) == 0:
                            print("No se encuentra ningun diccionario en memoria para guardar, aprete ENTER para volver")
                        else:    
                            bsbi.guardarIndiceInvertido(lista)
                            lista = []
                            print("Indice guardado, aprete ENTER para avanzar")
                        key2 = None
                        while key2 != b'\r':
                            key2 = msvcrt.getch()
                        if key2 == b'\r':
                            pass
                    elif ans2 == b"3":
                        try:
                            index = bsbi.recuperarIndice()
                            index2 = bsbi.recuperarListaDeIndiceDocID()
                            index3 = bsbi.recuperarListaDeIndiceTermID()
                            print("Indice cargado, aprete ENTER para avanzar")
                        except:
                            print("No se pudo encontrar alguno de los indices, aprete ENTER para volver atras")  
                        key2 = None
                        while key2 != b'\r':
                            key2 = msvcrt.getch()
                        if key2 == b'\r':
                            pass
                    elif ans2 == b"4":
                        break            
                os.system("cls")
        elif ans==b"3":
            print("\n WORK IN PROGRESS, apreta ENTER para volver")
            key = None
            while key != b'\r':
                key = msvcrt.getch()
            if key == b'\r':
                pass 
        elif ans==b"4":
            os.system('cls')
            print("Si desea volver atras presione la tecla Esc, si esta seguro de querer acceder al menu de BUSCAR PALABRA presione ENTER")
            key = None
            while key != b'\x1b' and key != b'\r':
                key = msvcrt.getch()
            if key == b'\x1b':
                pass
            else:
                os.system('cls')
                palabra = input("Ingrese una palabra:")
                os.system("cls")
                bsbi.encontrarNoticiasdePalabra(palabra, index)
           
                print("\nAprete enter para salir")
                key2=None
                while key2 != b"\r":
                    key2 = msvcrt.getch()
                if key2 == b'\r':
                    pass
        elif ans == b"5":
            ans = False     

