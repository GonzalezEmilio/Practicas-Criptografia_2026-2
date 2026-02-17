import random

def procesar_cesar(texto, desplazamiento):
    resultado = "" #Para que sea texto
    for caracter in texto:
        if caracter.isupper(): #Para Mayusculas
            resultado += chr((ord(caracter) - 65 + desplazamiento) % 26 + 65)
        elif caracter.islower(): #Para Minusculas
            resultado += chr((ord(caracter) - 97 + desplazamiento) % 26 + 97)
        else:
            resultado += caracter
    return resultado

def menu(): #Menu para el usuario
    while True:
        print("\n------ MENÚ CIFRADO CÉSAR ------")
        print("1. Cifrar mensaje ")
        print("2. Descifrar mensaje ")
        print("3. Salir")
        
        opcion = input("Selecciona una opción: ")

        if opcion == "1":
            mensaje = input("Introduce el mensaje a cifrar: ")
            clave_aleatoria = random.randint(1, 25) #Para que siempre sea diferente
            cifrado = procesar_cesar(mensaje, clave_aleatoria)
            print(f"\n Mensaje cifrado: {cifrado}")
            print(f" Clave generada aleatoriamente: {clave_aleatoria}")

        elif opcion == "2":
            mensaje = input("Introduce el mensaje a descifrar: ")
            print("\nOpciones de descifrado:")
            print("a) Con un número de desplazamiento conocido")
            print("b) Por fuerza bruta (probar todas las posibilidades)")
            sub_opcion = input("Selecciona (a/b): ").lower() #Acepta Mayusculas

            if sub_opcion == "a":
                clave = int(input("Introduce el desplazamiento: "))
                print(f"\n Resultado: {procesar_cesar(mensaje, -clave)}") #Debe ser negativo
            
            elif sub_opcion == "b":
                print("\n--- Probando todas las combinaciones ---") #Fuerza Bruta
                for i in range(1, 26): #Solo se pueden tener 25 desplazamientos en Cesar
                    intento = procesar_cesar(mensaje, -i)
                    print(f"Desplazamiento {i:02d}: {intento}")
            else:
                print("Opción no válida.")

        elif opcion == "3":
            print("Saliendo....")
            break
        else:
            print("Opción no reconocida, intenta de nuevo!!.")

if __name__ == "__main__":
    menu()
