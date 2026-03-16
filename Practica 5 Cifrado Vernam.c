#include <stdio.h>
#include <stdlib.h>
#include <string.h>

// Esta funcion convierte el valor a binario
void valor_a_binario(int valor, char *bin) {
    for (int i = 4; i >= 0; i--) {
        bin[i] = (valor & 1) ? '1' : '0';
        valor >>= 1;
    }
    bin[5] = '\0';
}

// Esta parte convierte una cadena binaria de 5 bits a valor de 0 a 25
int binario_a_valor(const char *bin) {
    int valor = 0;
    for (int i = 0; i < 5; i++) {
        valor = (valor << 1) | (bin[i] - '0');
    }
    return valor;
}

// Funcion para cifrar el mensaje usando bloques binarios de 5 bits y XOR
void cifrar_mensaje(const char *mensaje, const char *llave, char *cifrado, int longitud) {
    for (int i = 0; i < longitud; i++) {
        char letra_m = mensaje[i];
        char letra_k = llave[i];

        int val_m = letra_m - 'A';
        int val_k = letra_k - 'A';

        char bin_m[6], bin_k[6], bin_c[6];
        valor_a_binario(val_m, bin_m);
        valor_a_binario(val_k, bin_k);

        // XOR o tambien bit a bit
        for (int j = 0; j < 5; j++) {
            bin_c[j] = (bin_m[j] == bin_k[j]) ? '0' : '1';
        }
        bin_c[5] = '\0';

        int val_c = binario_a_valor(bin_c);
        char letra_c = 'A' + (val_c % 26);

        cifrado[i] = letra_c;
    }
    cifrado[longitud] = '\0';
}

// Funcion para descifrar el mensaje usando bloques binarios de 5 bits y XOR
void descifrar_mensaje(const char *cifrado, const char *llave, char *mensaje, int longitud) {
    for (int i = 0; i < longitud; i++) {
        char letra_c = cifrado[i];
        char letra_k = llave[i];

        int val_c = letra_c - 'A';
        int val_k = letra_k - 'A';

        char bin_c[6], bin_k[6], bin_m[6];
        valor_a_binario(val_c, bin_c);
        valor_a_binario(val_k, bin_k);

        // XOR o tambien bit a bit
        for (int j = 0; j < 5; j++) {
            bin_m[j] = (bin_c[j] == bin_k[j]) ? '0' : '1';
        }
        bin_m[5] = '\0';

        int val_m = binario_a_valor(bin_m);
        char letra_m = 'A' + (val_m % 26);

        mensaje[i] = letra_m;
    }
    mensaje[longitud] = '\0';
}
// Menu del programa
int main() {
    int opcion;
    char mensaje[1000], llave[1000], cifrado[1000], recuperado[1000];
    int longitud_mensaje, longitud_llave, longitud_cifrado;

    do {
        printf("\n--- Cifrado Vernam ---\n");
        printf("1) Cifrar\n");
        printf("2) Desencriptar\n");
        printf("3) Salir\n");
        printf("Selecciona una opcion: ");
        scanf("%d", &opcion);
        getchar();

        switch(opcion) {
            case 1: {
                printf("Ingresa el mensaje que deseas cifrar, recuerda que solo mayusculas de la A-Z y sin espacios: ");
                scanf("%s", mensaje);

                printf("Ingrese la llave, recuerda que solo mayusculas de la A-Z y de la misma longitud que el mensaje: ");
                scanf("%s", llave);

                longitud_mensaje = strlen(mensaje);
                longitud_llave = strlen(llave);

                if (longitud_mensaje != longitud_llave) {
                    printf("Error: la llave debe tener la misma longitud que el mensaje.\n");
                } else {
                    cifrar_mensaje(mensaje, llave, cifrado, longitud_mensaje);
                    printf("Mensaje cifrado: %s\n", cifrado);
                }
                break;
            }

            case 2: {
                printf("Ingresa el mensaje cifrado, recuerda que solo mayusculas de la A-Z y sin espacios: ");
                scanf("%s", cifrado);

                printf("Ingresa la llave, recuerda que solo mayusculas de la A-Z y de la misma longitud que el mensaje cifrado: ");
                scanf("%s", llave);

                longitud_cifrado = strlen(cifrado);
                longitud_llave = strlen(llave);

                if (longitud_cifrado != longitud_llave) {
                    printf("Error: la llave debe tener la misma longitud que el mensaje cifrado.\n");
                } else {
                    descifrar_mensaje(cifrado, llave, recuperado, longitud_cifrado);
                    printf("Mensaje desencriptado: %s\n", recuperado);
                }
                break;
            }

            case 3:
                printf("Hasta luego...!!!\n");
                break;

            default:
                printf("Opcion no valida\n");
        }
    } while(opcion != 3);

    return 0;
}