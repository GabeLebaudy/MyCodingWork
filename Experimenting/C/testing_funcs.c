#include <stdio.h>

void inc (int *q) {
    (*q)++;
}

int diagonal (int x[][3]) {
    int l = 0;
    int w = 2;
    int final = 0;
    while (l < 3) {
        final += x[l][l];
        final += x[l][w];
        l++;
        w--;
    }
    return final;
}

void swap (char *x, char *y) {
    while (*x != '\0' && *y != '\0') {
        char temp = *x;
        *x = *y;
        *y = temp;
        x++;
        y++;
    }
}

void concatAll (char **x, int n, char final[]) {
    int total_count = 0;
    for (int i = 0; i < n; i++) {
        char *current = x[i];
        while (*current != '\0') {
            final[total_count] = *current;
            current++;
            total_count++;
        }
    }
    final[total_count] = '\0';
}

int main() {
    int x = 1;
    inc(&x);
    printf("%d\n", x);
    int y[3][3] = {{1, 2, 3}, {4, 5, 6}, {7, 8, 9}};
    int result = diagonal(y);
    printf("%d\n", result);
    char str1[] = "abc";
    char str2[] = "defghij";
    swap(str1, str2);
    printf("%s,%s\n", str1, str2);

    char *x1 = "abc";
    char *x2 = "defghi";
    char *x3 = "z";
    char *xs[] = {x1, x2, x3};
    int n = sizeof(xs) / sizeof(char *);
    char dest[11];
    concatAll(xs, n, dest);
    printf("%s\n", dest);
}