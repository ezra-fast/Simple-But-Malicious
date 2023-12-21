#include <stdio.h>
#include <io.h>

int main() {
    const char *filename = "path/to/your/file.txt";

    // Check if the file is writable
    if (_access(filename, 02) == 0) {               // 00 is for existence, 02 is for write permissions, 04 is for read permissions, and 06 is for both read and write permissions
        printf("File is writable\n");               // docs: https://learn.microsoft.com/en-us/cpp/c-runtime-library/reference/access-waccess?view=msvc-170
    } else {
        printf("File is not writable\n");
    }

    return 0;
}


// The below is POSIX

// #include <stdio.h>
// #include <unistd.h>
// #include <stdbool.h>

// int is_folder_writable(char* str);

// int main() {
//     char path[200];

//     strcpy(path, "C:\\ProgramData");

//     // printf("Enter a directory path: ");
//     // scanf("%199s", path);

//     printf("result: %d\n", is_folder_writable(path));

//     return 0;
// }

// int is_folder_writable(char* str) {
//     if(access(str, W_OK) == 0) {
//         return 1;
//     } else {
//         return -1;   
//     }
// }