/*
Author: Ezra Fast
Date: July 6th, 2023
Description: This code is run with either --encrypt or --decrypt and will call the respective function on the file specified during runtime.
	The encryption process is a simple XOR but the function can be adjusted to be more comprehensive. The function is called on each byte of 
	the input file independently. This produces a Windows specific executable.
	You must use the same numeric key to encrypt and decrypt the file, otherwise you will just encrypt it further :) 
*/
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <getopt.h>
#include <windows.h>				// Windows System programming is the reason I am now using Python.

int * key_retriever(int * pointer_to_key_location);
void argument_checker(char string[]);
void usage_indicator(void);
BYTE simple_encrypt(BYTE the_byte, int the_key);
BYTE simple_decrypt(BYTE character, int the_key);
unsigned char same_or_new(char option[]);

int main(int argc, char * argv[]) {

	int decider = 0;

	if (argc != 2) {
		usage_indicator();
	}
	else if (argc == 2) {
		argument_checker(argv[1]);
	}
	
	int * KEY;
	KEY = key_retriever(KEY);

	// This is the start of the getopt_long() mess
	
	int opt = 0;
	
	static struct option long_options[] = {
		{"decrypt", no_argument, 0, 'd'},
		{"encrypt", no_argument, 0, 'e'},
		{0, 0, 0, 0}
	};
	
	int long_index = 0;
	while ((opt = getopt_long(argc, argv, "e::d::", long_options, &long_index)) != -1) {		// the cmdline input following an option can be accessed in 'optarg'
		switch (opt) {
			case 'e':
				decider = 1;
				break;
			case 'd':
				decider = 2;
				break;
			default:
				usage_indicator();
				exit(-1);
		}
	}
	
	// This is the end of the getopt_long() mess; 		decider will be 1 for encryption, 2 for decryption;

	char input_filename[20];
	printf("Enter the input file: ");
	scanf("%s", input_filename);

	/* This is the start of the Windows System programming; Making a file handle, map the file to memory, create a file view, 
	operate on the file, flush the changes to disk, unmap the file from memory, close the file handle */
	
	HANDLE fileHandle, fileMapping;
	LPVOID fileView;
	
	// Establishing a file handle:
	fileHandle = CreateFile(input_filename, GENERIC_READ | GENERIC_WRITE, 0, NULL, OPEN_EXISTING, FILE_ATTRIBUTE_NORMAL, NULL);
	
	if (fileHandle == INVALID_HANDLE_VALUE) {
		printf("Failed to establish file handle\n");
		exit(-1);
	}
	
	// Map the file to memory:
	fileMapping = CreateFileMapping(fileHandle, NULL, PAGE_READWRITE, 0, 0, NULL);
	if (fileMapping == NULL) {
		printf("Problem mapping the file\n");
		CloseHandle(fileMapping);		// Explore why these two lines are necessary
		CloseHandle(fileHandle);
		exit(-1);
	}
	
	// Create a file view:
	fileView = MapViewOfFile(fileMapping, FILE_MAP_ALL_ACCESS, 0, 0, 0);
	if (fileView == NULL) {
		printf("Problem creating file view\n");
		CloseHandle(fileMapping);
		CloseHandle(fileHandle);
		exit(-1);
	}
	
	// file view: fileView, file mapping: fileMapping, file handle: fileHandle
	
	LARGE_INTEGER fileSize;
	GetFileSizeEx(fileHandle, &fileSize);
	DWORD fileLength = fileSize.LowPart;
	
	int for_counter = 0;
		
	char mode[20];			// Determining the mode of the program
	if (decider == 1) {
		strcpy(mode, "encrypt");
	}
	else if (decider == 2) {
		strcpy(mode, "decrypt");
	}
	else if (decider != 1 && decider != 2) {
		printf("Invalid Option\n");
		exit(-1);
	}
	
	if (decider == 1) {					// Encryption
		
		unsigned char file_choice = same_or_new(mode);
		
		file_choice = toupper(file_choice);
		
		if (file_choice == 'S') {		
			BYTE * fileBytes = (BYTE *)fileView;
			BYTE byteValue = fileBytes[0];
			for (for_counter = 0; byteValue != EOF; for_counter++) {
				byteValue = fileBytes[for_counter];
				byteValue = simple_encrypt(byteValue, *KEY);
				fileBytes[for_counter] = byteValue;
			}
			/* do {
				// BYTE * fileBytes = (BYTE*)fileView;		// fileBytes is a BYTE pointer to the current byte of the mem mapped material
				// BYTE byteValue = fileBytes[2];		// byteValue is a way of variablizing the content at the fileBytes pointer --> think of it as an array
				
			} while (byteValue != EOF);
			*/
		}
		else if (file_choice == 'N') {
			char output_filename[20];
			printf("Enter the name of the output file: ");
			scanf("%s", output_filename);
			
			FILE * output_file = fopen(output_filename, "w");
			
			do {
				current_char = 
			} while (current_char != EOF);		// Pick up here.
		}
	}
	else if (decider == 2) {				// Decryption
		BYTE * fileBytes = (BYTE *)fileView;
		BYTE byteValue = fileBytes[0];
		for (for_counter = 0; byteValue != EOF; for_counter++) {
			byteValue = fileBytes[for_counter];
			byteValue = simple_decrypt(byteValue, *KEY);
			fileBytes[for_counter] = byteValue;
		}
		/* BYTE * fileBytes = (BYTE*)fileView;			
		BYTE byteValue = fileBytes[2];
		printf("value: %c\n", byteValue);
		fileBytes[2] += 20;
		printf("new value: %c\n", fileBytes[2]); */
	}
	// to write:
	// fileBytes[offset] = byteValue;


	// This is the second episode of the Windows API programming catastrophe:
	// Flush changes to disk:
	FlushViewOfFile(fileView, 0);
	
	// Unmapping from memory:
	UnmapViewOfFile(fileView);
	CloseHandle(fileMapping);
	
	// Closing the file handle:
	CloseHandle(fileHandle);

	return 0;
} // This is the end of the main() function

BYTE simple_encrypt(BYTE the_byte, int the_key) {
	the_byte = the_byte ^ the_key;
	return the_byte;
}

BYTE simple_decrypt(BYTE character, int the_key) {
	character = character ^ the_key;
	return character;
}

void usage_indicator(void) {
	printf("Usage: cryptography.exe --encrypt or --decrypt\n");
	exit(-1);
}

void argument_checker(char string[]) {
	if (strcmp(string, "--encrypt") != 0 && strcmp(string, "--decrypt") != 0) {
		usage_indicator();
		exit(-1);
	}
}

int * key_retriever(int * pointer_to_key_location) {
	printf("Please enter a numeric symmetric key: ");
	scanf("%d", pointer_to_key_location);
	return pointer_to_key_location;
}

unsigned char same_or_new(char option[]) {
	fflush(stdin); 
	unsigned char the_choice;
	printf("Enter N for new file, S to %s the same file: ", option);
	scanf("%c", &the_choice);
	return the_choice;
}