#include <stdio.h>
#include <stdlib.h>
#include <string.h>

unsigned char simple_encrypt(char character, int key);
unsigned char simple_decrypt(char character, int key);

#define KEY 67

int main(int argc, char * argv[]) {

	// char output_filename[15];

	// printf("Please enter the name of the output file: ");
	// scanf("%s", output_filename);

	// printf("%s", output_filename);		// Debugging Line

	FILE * file = fopen(argv[1], "r+");
	FILE * output = fopen(argv[2], "w+");
	
	if (file == NULL) {
		printf("Error opening the input file\n");
		return -1;
	}

	if (output == NULL) {
		printf("Error opening the output file\n");
		return -1;
	}

	char current_char;

	do {
		if (feof(file) != 0) {
			break;
		}
		current_char = fgetc(file);
		if (current_char == EOF) {
			break;
		}
		current_char = simple_encrypt(current_char, KEY);
		fputc(current_char, output);
	} while (feof(file) == 0);

	fclose(output);
	fclose(file);
	return 0;
}

unsigned char simple_encrypt(char character, int key) {
	character = character ^= key;
	character = character += 20;
	return character;
}

unsigned char simple_decrypt(char character, int key) {
	character = character -= 20;
	character = character ^= key;
	return character;
}