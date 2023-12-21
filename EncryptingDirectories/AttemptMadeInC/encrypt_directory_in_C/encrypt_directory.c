/** This code will traverse the specified directory and encrypt all material therein. **/
// Author: Ezra Fast
// Date: July 19, 2023
 
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <dirent.h>
#include <stdbool.h>
#include <sys/stat.h>
#include <windows.h>>

int is_directory(const char* path);
int directory_checker(DIR * directory);
int directory_encryptor(DIR * directory);

int main(int argc, char **argv) {

    char dir_name[75] = {"C:\\Users\\efast\\OneDrive - Calgary Stampede\\Documents\\encryption_practice"};
    printf("%s", dir_name);

    DIR * directory;
    directory = opendir(dir_name);
    if (directory == NULL) {
        printf("Directory could not be opened.\n");
        exit(-1);
    }

    directory_encryptor(directory);        

    closedir(directory);
    return 0;
}

int directory_encryptor(DIR * directory) {
    struct dirent * directory_entry;
    int number_of_files = 0;
    while ( (directory_entry = readdir(directory)) ) {
        // This is unfinished, resume here.
        printf("Entry: %s%s\n", , directory_entry->d_name);
        number_of_files++;
    }
}

int directory_checker(DIR * directory) {
    if (directory == NULL) {
        perror("Failed to open directory\n");
        exit(-1);
    }
    else {
        printf("The Directory has been opened\n");
        return 0;
    }
}

int is_directory(const char* path) {
    struct stat stat_buffer;
    if (stat(path, &stat_buffer) == -1) {
        perror("stat");
        return 1;       // This means its a file? 
    }
    // return S_ISDIR(stat_buffer.st_mode);
    return 0;           // This means its a directory presumably?
}
