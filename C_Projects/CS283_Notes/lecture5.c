#include <stdio.h>

//Converts ASCII representation of a number in a file to its decimal value. (Used in scanf).
int str2int(char *s, int b) {
    int n;
    char *p;
    
    n = 0;
    for (p = s; p != '\0';p++) {
        if (*p <= 9) {
            n = n * b + *p - '0';
        } else {
            n = n * b + *p - 'a' + 10;
        }
    }
    return n;
}

int main() {
    return 0;
}