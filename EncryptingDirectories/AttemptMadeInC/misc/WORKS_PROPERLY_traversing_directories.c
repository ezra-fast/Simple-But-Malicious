/* 

* Author: Ezra Fast / the internet; Date: August 2, 2023;
* Description: This will traverse the given directory recursively and, when used with the --dump option, will dump the contents of all files in directory and sub-directory to the console.

* From Here: This can be used to recursively encrypt entire directories. Given that characters are written to the console one at a time, it would be easiest to implement a stream cipher
*            for starters. Modify line 116 to read the bytes from the file instead of chars, and apply an operation to the bytes to accomplish this.

* To evade detection from debuggers in the event this code becomes malicious, there are starting points for these techniques in the file CRE.c

*/
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <dirent.h>
#include <sys/stat.h>
#include <sys/types.h>

void show_file_contents(const char *path);
void traverse(char * base_path, int indentation, int dump_files_flag);
void check_validity_of_directory(char * directory_base_path);
int dump_flag_setter(char * arg);

int main(int argc, char *argv[]) {

	int dump_flag;

	if (argv[1]) {
		dump_flag = dump_flag_setter(argv[1]);
	} else {
		dump_flag = 0;
	}
	
	char directory_base_path[200];
	
	strcpy(directory_base_path, "C:\\Users\\efast\\OneDrive - Calgary Stampede\\Documents\\personal\\encryption_practice");
	
	// printf("Enter the directory path: ");
	// fgets(directory_base_path, sizeof(directory_base_path), stdin);
	// directory_base_path[strcspn(directory_base_path, "\n")] = '\0';		// cracked way of removing character at end of line

	printf("\n");

	check_validity_of_directory(directory_base_path);

	printf("Traversing: %s\n\n", directory_base_path);
	
	traverse(directory_base_path, 0, dump_flag);	

	printf("\n");
	return 0;
}

void check_validity_of_directory(char * directory_base_path) {
	if (opendir(directory_base_path) == NULL) {
		printf("Invalid Path Given\n");
		exit(-1);
	}
}

void traverse(char * base_path, int indentation, int dump_files_flag) {
	
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
			
			if (dump_files_flag) {
				printf("\n");
				show_file_contents(path);
			}
								// The base case of the recursion will have the most amount of indentation (or the least? whatever...)
			traverse(path, indentation + 1, dump_files_flag);	// indentation seems to recede in the output after it gets larger, remember this is recursive.
		}
	}
	closedir(dir);
}

void show_file_contents(const char *path) {
	printf("---------- BEGINNING OF CONTENT ----------\n");
	struct stat path_stat;

	if (stat(path, &path_stat) != 0) {
		perror("Error getting file/directory information\n");
	}

	if (S_ISDIR(path_stat.st_mode)) {
		printf("Directory encountered.\n\n");
	} 
	else if (S_ISREG(path_stat.st_mode)) {
		FILE *file = fopen(path, "r");
		if (file == NULL) {
		perror("Error opening file\n");
	}

		char c;
		while ((c = fgetc(file)) != EOF) {
			putchar(c);
		}

		fclose(file);
	} 
	else {
		printf("The provided path is neither a file nor a directory.\n");
	}
	printf("---------- END OF CONTENT ----------\n");
	printf("\n");
}

int dump_flag_setter(char * arg) {
	if (strcmp(arg, "--dump") == 0) {
		return 1;
	} else {
		return 0;
	}
}