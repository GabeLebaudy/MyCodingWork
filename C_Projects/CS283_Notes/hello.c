#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <string.h>

int
main() {
    char buf[1024];

    strcpy(buf, "Hello ");
    strcpy(buf + 6, "World");
    strcpy(buf + 11, "\n");
    write(1, buf, strlen(buf));

/*
    printf("Hello World\n");
*/
}