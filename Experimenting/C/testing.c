#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <errno.h>

struct Point{
    int x;
    int y;
};

int main() {
    struct Point p = {5, 10};
    printf("%d", p.x);
    return 0;
}