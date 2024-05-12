#include <stdio.h>
#include <stdlib.h>
#include <math.h>

int main(int argc, char *argv[]) {
    if (argc != 3) {
        printf("Error: 2 Arguments must be provided.");
        return 1;
    }

    char *name = argv[1];
    double radius = atof(argv[2]);
    double pi = M_PI;

    double area = pi * radius * radius;

    printf("%s, your area is %.3e units squared.", name, area);
    return 0;
}