import msvcrt
import os
from recolector import Recolector
from bsbi import FuncionesBSBI
from termcolor import colored
from crear_binarios import Bit_array

class Menu:

    def __init__(self):
        self.recolector = Recolector()
        self.bsbi = FuncionesBSBI()
        self.ans=True
        self.index = {}
        self.lista = []
        self.compresor = Bit_array()
        self.intArrayBinario = []

    
    def ejecutarMenu(self):

        while self.ans:
            os.system("cls")
            print ("""
            1.Recolectar noticias
            2.Crear indice invertido
            3.Mostar el indice invertido en memoria
            4.Realizar busquedas
            5.Compresion de lista de apariciones
            6.Salir del programa
            """)

            print(colored("Ingrese la opcion deseada:", "blue"))
            self.ans=msvcrt.getch()

            if self.ans==b"1": 
                os.system('cls')
                print(colored("Si desea volver atras presione la tecla Esc, si esta seguro de querer recolectar noticias presione ENTER", "yellow"))
                self.key = None
                while self.key != b'\x1b' and self.key != b'\r':
                    self.key = msvcrt.getch()
                if self.key == b'\x1b':
                    pass
                else:
                    os.system("cls")
                    self.recolector.descargarNoticias()

            elif self.ans==b"2":
                os.system('cls')
                print(colored("Si desea volver atras presione la tecla Esc, si esta seguro de querer acceder al menu de Indices Invertidos presione ENTER", "yellow"))
                self.key = None
                while self.key != b'\x1b' and self.key != b'\r':
                    self.key = msvcrt.getch()
                if self.key == b'\x1b':
                    pass
                else:

                    self.ans2=True
                    while(self.ans2):

                        os.system("cls")
                        print ("""
                        1.Crear indice desde directorio
                        2.Guardar indice en disco
                        3.Cargar indice previamente salvado
                        4.Volver atras
                        """)

                        print(colored("Ingrese la opcion deseada:", "blue"))
                        self.ans2=msvcrt.getch()

                        if self.ans2 ==b"1":
                            self.temp = self.bsbi.mainIndiceInvertido()
                            self.index = self.temp[0]
                            self.lista = self.temp[1]
                            print(colored("Indice creado, aprete ENTER para avanzar", "green"))
                            self.key2 = None
                            while self.key2 != b'\r':
                                self.key2 = msvcrt.getch()
                            if self.key2 == b'\r':
                                pass
                        elif self.ans2 == b"2":
                            os.system("cls")
                            if len(self.lista) == 0:
                                print(colored("No se encuentra ningun diccionario en memoria para guardar, aprete ENTER para volver", "red"))
                            else:    
                                self.bsbi.guardarIndiceInvertido(self.lista)
                                self.lista = []
                                print(colored("Indice guardado, aprete ENTER para voler", "green"))
                            self.key2 = None
                            while self.key2 != b'\r':
                                self.key2 = msvcrt.getch()
                            if self.key2 == b'\r':
                                pass
                        elif self.ans2 == b"3":
                            os.system("cls")
                            try:
                                self.index = self.bsbi.recuperarIndice()
                                self.index2 = self.bsbi.recuperarListaDeIndiceDocID()
                                self.index3 = self.bsbi.recuperarListaDeIndiceTermID()
                                print(colored("Indice cargado, aprete ENTER para avanzar", "green"))
                            except:
                                print(colored("No se pudo encontrar alguno de los indices, aprete ENTER para volver atras", "red"))  
                            self.key2 = None
                            while self.key2 != b'\r':
                                self.key2 = msvcrt.getch()
                            if self.key2 == b'\r':
                                pass
                        elif self.ans2 == b"4":
                            break            
                    os.system("cls")
            elif self.ans==b"4":
                os.system('cls')
                print("Si desea volver atras presione la tecla Esc, si esta seguro de querer acceder al menu de BUSCAR PALABRA presione ENTER")
                self.key = None
                while self.key != b'\x1b' and self.key != b'\r':
                    self.key = msvcrt.getch()
                if self.key == b'\x1b':
                    pass
                else: 
                    os.system('cls')     
                    self.palabra = input(colored("Ingrese una palabra:", "blue"))
                    os.system("cls")
                
    
                    self.intArrayComprimido = self.compresor.obtener_tajadas_binarias_de_int_array_comprimido()
                    self.bsbi.encontrarNoticiasdePalabraComprimida(self.palabra, self.index, self.intArrayComprimido)
                    print("\nAprete enter para salir")
                    self.key2=None
                    while self.key2 != b"\r":
                        self.key2 = msvcrt.getch()
                    if self.key2 == b'\r':
                        pass
            elif self.ans == b"3":
                os.system("cls")
                if len(self.index) == 0:
                    print(colored("No se encuentra ningun diccionario en memoria, aprete ENTER para volver", "red"))
                else:
                    print(self.index, colored("\nAprete ENTER para volver", "green"))
                self.key = None
                while self.key != b'\r':
                    self.key = msvcrt.getch()
                if self.key == b'\r':
                    pass              
            elif self.ans == b"5":

                os.system("cls")
                if len(self.index) == 0:
                    print(colored("No se encuentra ningun diccionario en memoria, aprete ENTER para volver", "red"))
                else:
                    self.intArray = self.bsbi.recuperarIntArray()
                    self.compresor.ejecutar_compresion_y_guardar_en_disco(self.intArray, self.index)
                    print(colored("\nLista de apariciones comprimida. Aprete ENTER para volver", "green"))
                    self.key = None
                    while self.key != b'\r':
                        self.key = msvcrt.getch()
                    if self.key == b'\r':
                        pass 
            elif self.ans == b"6":
                self.ans == False
x = Menu()
x.ejecutarMenu()