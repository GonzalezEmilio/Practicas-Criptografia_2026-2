from typing import List, Tuple, Dict

def limpiar_texto(texto: str) -> str:
    texto = texto.lower().replace(" ", "")
    texto = "".join(ch for ch in texto if "a" <= ch <= "z")
    return texto.replace("j", "i")

def preparar_pares(mensaje: str) -> str:
    m = list(mensaje)
    if len(m) % 2 == 1:
        m.append("x")
    for i in range(0, len(m), 2):
        if m[i] == m[i + 1]:
            m[i + 1] = "x"
    return "".join(m)

def postprocesar_descifrado(mensaje: str) -> str:
    if mensaje.endswith("x"):
        mensaje = mensaje[:-1]
    m = list(mensaje)
    for i in range(0, len(m) - 1, 2):
        if m[i + 1] == "x":
            m[i + 1] = m[i]
    return "".join(m)

def generar_matriz(llave: str) -> Tuple[List[List[str]], Dict[str, Tuple[int, int]]]:
    llave = limpiar_texto(llave)
    usados = [False] * 26
    letras: List[str] = []

    for ch in llave:
        idx = ord(ch) - ord("a")
        if not usados[idx]:
            usados[idx] = True
            letras.append(ch)

    for code in range(ord("a"), ord("z") + 1):
        ch = chr(code)
        if ch == "j":
            continue
        idx = code - ord("a")
        if not usados[idx]:
            usados[idx] = True
            letras.append(ch)

    matriz = [letras[r * 5:(r + 1) * 5] for r in range(5)]
    pos = {matriz[r][c]: (r, c) for r in range(5) for c in range(5)}
    return matriz, pos

def imprimir_matriz(matriz: List[List[str]]) -> None:
    for fila in matriz:
        print(" ".join(fila))

def encriptar(mensaje: str, matriz: List[List[str]], pos: Dict[str, Tuple[int, int]]) -> str:
    m = list(mensaje)
    for i in range(0, len(m), 2):
        a, b = m[i], m[i + 1]
        ra, ca = pos[a]
        rb, cb = pos[b]

        if ra == rb:  # misma fila -> derecha
            m[i] = matriz[ra][(ca + 1) % 5]
            m[i + 1] = matriz[rb][(cb + 1) % 5]
        elif ca == cb:  # misma columna -> abajo
            m[i] = matriz[(ra + 1) % 5][ca]
            m[i + 1] = matriz[(rb + 1) % 5][cb]
        else:
            # rectangulo: misma fila, columna de la otra letra
            m[i] = matriz[ra][cb]
            m[i + 1] = matriz[rb][ca]

    return "".join(m)

def desencriptar(mensaje: str, matriz: List[List[str]], pos: Dict[str, Tuple[int, int]]) -> str:
    m = list(mensaje)
    for i in range(0, len(m), 2):
        a, b = m[i], m[i + 1]
        ra, ca = pos[a]
        rb, cb = pos[b]

        if ra == rb:  # misma fila -> izquierda
            m[i] = matriz[ra][(ca + 4) % 5]
            m[i + 1] = matriz[rb][(cb + 4) % 5]
        elif ca == cb:  # misma columna -> arriba
            m[i] = matriz[(ra + 4) % 5][ca]
            m[i + 1] = matriz[(rb + 4) % 5][cb]
        else:
            # rectangulo (misma regla)
            m[i] = matriz[ra][cb]
            m[i + 1] = matriz[rb][ca]

    return "".join(m)

def main():
    mensaje_in = input("Ingresa el mensaje:\n")
    llave_in = input("\nIngresa la llave:\n")

    mensaje_plano = limpiar_texto(mensaje_in)
    llave = limpiar_texto(llave_in)

    matriz, pos = generar_matriz(llave)

    # Se guarda el último cifrado para que en la opcion dos no se no pida de nuevo.
    ultimo_cifrado = None

    mensaje_preparado = preparar_pares(mensaje_plano)
    print(f"\nMensaje ingresado: {mensaje_plano}")
    print(f"Mensaje preparado: {mensaje_preparado}\n")
    print(f"Llave ingresada: {llave}\n")

    print("Matriz:")
    imprimir_matriz(matriz)
    print()

    while True:
        print("Ingresa la opción que deseas:")
        print("1) Encriptar")
        print("2) Desencriptar")
        print("3) Salir")

        try:
            opcion = int(input("> ").strip())
        except ValueError:
            print("\nOpcion incorrecta. Ingresa una opción válida.\n")
            continue

        print()

        if opcion == 1:
            # Se cifra a partir del texto plano limpio como el ejemplo de clase
            mensaje_preparado = preparar_pares(mensaje_plano)
            ultimo_cifrado = encriptar(mensaje_preparado, matriz, pos)

            print("El mensaje se encriptó como:")
            print(ultimo_cifrado, "\n")

        elif opcion == 2:
            # Si ya hay cifrado guardado, se usa ese.
            if ultimo_cifrado is None:
                entrada = input("No hay un cifrado guardado. Ingresa el texto cifrado:\n")
                entrada = limpiar_texto(entrada)
                if len(entrada) % 2 == 1:
                    print("\nError: el texto cifrado debe tener longitud par.\n")
                    continue
                ultimo_cifrado = entrada

            desc = desencriptar(ultimo_cifrado, matriz, pos)
            plano = postprocesar_descifrado(desc)

            print("\nEl mensaje se descencriptó como:")
            print(plano, "\n")

            # Se deja el estado listo por si se vuelve a cifrar/descifrar
            mensaje_plano = plano
            ultimo_cifrado = None

        elif opcion == 3:
            print("¡Hasta luego!")
            break
        else:
            print("Ingresa otra opción.\n")

if __name__ == "__main__":
    main()