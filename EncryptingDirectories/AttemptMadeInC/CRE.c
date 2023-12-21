#include <string.h>
#include <stdio.h>
#include <stdlib.h>
#include <windows.h>
#include <stdbool.h>

/** 
Anti Debugging Techniques employed in this code:
	
	Checking for a user mode debugger --> IsDebuggerPresent()
	Checking for breakpoints by checking memory for 0xCC
	Not Implemented:	Checking for execution time --> time between routines > 0.1 is cause to enter infinite loop
	
**/

int debugger_checker(void);
void breakpoint_detector(void);
char reveal(char input);
char changer(char input);


int main(int argc, char ** argv) {				// Main function begins here
	breakpoint_detector();
	debugger_checker();
	


	return 0;
}

int debugger_checker(void) {
	int result = IsDebuggerPresent();
	if (result != 0) {
		printf("Debugger Emergency\n");
		while(1) {
			printf("				");
		}
	}
	return 0;
}

void breakpoint_detector(void) {						// This function may not work as well as the Windows API function
	volatile char * break_point;					// Frankly, I don't even know if this works
	if (*break_point == 0xCC) {
		printf("Debugger Emergency\n");
		exit(-1);
	}
}