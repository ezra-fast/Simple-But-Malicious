#include <stdio.h>

int main(int argc, char **argv) {
    const char *filename = argv[1];
    FILE * file = fopen(filename, "rb+");

    int byte;

    while ((byte = fgetc(file)) != EOF) {
        byte ^= 12;
        fseek(file, -1, SEEK_CUR);
        fputc(byte, file);
        fseek(file, 0, SEEK_CUR);
    }
    fclose(file);
    return 0;
}