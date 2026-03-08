import numpy as np

ALFABETO = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"  # Alfabeto de la A a la Z
MODULO = 26

def normalizar_texto(texto):
    # Se convierte a mayusculas y elimina espacios
    return texto.upper().replace(" ", "")

def preparar_texto(texto):
    # Se limpia el texto y se asegura que sea de longitud par para la matriz 2x2
    texto = normalizar_texto(texto)

    # Se valida que solo tenga letras del alfabeto
    if not all(letra in ALFABETO for letra in texto):
        raise ValueError("El texto contiene caracteres no validos. Solo se permiten letras de la A a la Z.")

    # Si la longitud es impar, se agrega una X
    if len(texto) % 2 != 0:
        texto += 'X'

    return texto

def validar_texto_cifrado(texto):
    if len(texto) == 0:
        raise ValueError("El texto cifrado no puede estar vacio.")

    if " " in texto:
        raise ValueError("El texto cifrado no debe contener espacios.")

    if len(texto) % 2 != 0:
        raise ValueError("El texto cifrado debe tener una cantidad par de letras.")

    if not all(letra in ALFABETO for letra in texto):
        raise ValueError("Lo que ingresaste es invalido. Agrega un texto cifrado valido en mayusculas, usando solo letras de la A a la Z.")

    return texto

def cifrar(texto, clave):
    texto = preparar_texto(texto)
    cifrado = ""

    # Se procesa el texto en bloques de 2 letras
    for i in range(0, len(texto), 2):
        # Se convierten las 2 letras a sus valores numericos
        vector_p = np.array([
            ALFABETO.index(texto[i]),
            ALFABETO.index(texto[i + 1])
        ])

        # Se multiplica la matriz por el vector, aplicando modulo 26
        vector_c = np.dot(clave, vector_p) % MODULO

        # Se convierten los numeros resultantes de vuelta a letras
        cifrado += ALFABETO[vector_c[0]] + ALFABETO[vector_c[1]]

    return cifrado

def obtener_matriz_inversa(clave):
    # Se calcula la matriz inversa en modulo 26
    # Primero se obtiene el determinante de la matriz 2x2
    det = int(np.round(np.linalg.det(clave)))

    # Se calcula el inverso multiplicativo del determinante en modulo 26
    # Si esto falla, significa que la matriz elegida no sirve como llave
    try:
        det_inv = pow(det % MODULO, -1, MODULO)
    except ValueError:
        raise ValueError("La matriz llave no tiene inversa en modulo 26. Elige otra.")

    # Se calcula la matriz adjunta
    adjunta = np.array([
        [clave[1][1], -clave[0][1]],
        [-clave[1][0], clave[0][0]]
    ])

    # Se multiplica la adjunta por el inverso del determinante y se aplica el modulo
    inversa = (det_inv * adjunta) % MODULO
    return inversa

def descifrar(texto_cifrado, clave):
    # Validar y normalizar el texto cifrado
    texto_cifrado = validar_texto_cifrado(texto_cifrado)

    # Se obtiene la matriz inversa para revertir la multiplicacion original
    inversa = obtener_matriz_inversa(clave)
    descifrado = ""

    for i in range(0, len(texto_cifrado), 2):
        vector_c = np.array([
            ALFABETO.index(texto_cifrado[i]),
            ALFABETO.index(texto_cifrado[i + 1])
        ])

        # Se multiplica la matriz inversa por el vector cifrado
        vector_p = np.dot(inversa, vector_c) % MODULO
        descifrado += ALFABETO[int(vector_p[0])] + ALFABETO[int(vector_p[1])]

    return descifrado

def menu():
    # NOTA: La matriz llave es fija y es:
    # [3, 3]
    # [2, 5]
    clave = np.array([[3, 3], [2, 5]])

    while True:
        print("\n" + "=" * 25)
        print("   CIFRADO HILL   ")
        print("=" * 25)
        print("Ingresa la opcion que deseas:")
        print("1. Cifrar un mensaje")
        print("2. Descifrar un mensaje")
        print("3. Salir")

        opcion = input("\nElige una opcion: ")

        if opcion == '1':
            texto = input("Ingresa el texto que deseas cifrar: ")
            try:
                resultado = cifrar(texto, clave)
                print(f"\nEl texto cifrado es: {resultado}")
            except ValueError as e:
                print(f"\n[-] {e}")

        elif opcion == '2':
            texto = input("Ingresa el texto cifrado: ")
            try:
                resultado = descifrar(texto, clave)
                print(f"\nEl texto descifrado es: {resultado}")
            except ValueError:
                print("\nEl mensaje ingresado es invalido. Escribe un texto cifrado valido.")

        elif opcion == '3':
            print("\nHasta luego!")
            break
        else:
            print("\nLa opcion elegida no es valida. Elige una opcion valida.")

if __name__ == "__main__":
    menu()