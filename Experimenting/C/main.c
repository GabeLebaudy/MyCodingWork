#include <stdio.h>
#include "funcs.c"

int main(){
    int x[] = {77, 4, 8, 1, -100, 66};
    int n = sizeof(x) / sizeof(int);
    printf("%d\n", find(x, n, 77)); // prints 0
    printf("%d\n", find(x, n, 1)); // prints 3
    printf("%d\n", find(x, n, 66)); // prints 5
    printf("%d\n", find(x, n, 999)); // prints -1
    char y[] = "abcDefG HIjzkL ::: q";
    uppercase(y);
    printf("%s\n", y);
    int num = 3274;
    char z[5];
    int2str(num, z);
    printf("%s\n", z);
}