#include <stdio.h>
#include <stdlib.h>
#include <string.h>

int main(int argc, char * argv[]) {

	FILE * file = fopen(argv[1], "r+");
	
	if (file == NULL) {
		printf("Error opening the file\n");
		return -1;
	}

	int current_char;

	do {
		current_char = fgetc(file);
	
		printf("%c", current_char);
	} while (feof(file) == 0);

	fclose(file);
	return 0;
}