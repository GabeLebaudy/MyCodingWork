#include <stdio.h>
#include <string.h>

int main() {
    if (strstr("some sentence with for in it", "for") != NULL) {
        printf("Yes!");
    } else {
        printf("No!");
    }
}