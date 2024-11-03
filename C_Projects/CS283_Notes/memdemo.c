#include <stdio.h>

long gint;

int main() {
    long lint;
    void *vp;
    unsigned char *cp;

    gint = 4407873;
    lint = 6513249;

    printf("gint = %ld = %lx\n", gint, (unsigned long)gint);
    printf("gint is at address %p\n", &gint);
    printf("lint = %ld = %lx\n", lint, (unsigned long)lint);
    printf("lint is at address %p\n", &lint);
    printf("main is at address %p\n", main);

    vp = &gint;
    cp = vp;

    printf("%x, %x, %x, %x, %s\n", cp[0], cp[1], cp[2], cp[3], cp);

    vp = &lint;
    cp = vp;
    printf("%x, %x, %x, %x, %s\n", cp[0], cp[1], cp[2], cp[3], cp);
}