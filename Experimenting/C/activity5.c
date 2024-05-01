#include <stdio.h>

int mystrlen(char x[]) {
   int count = 0;
   while(*x != '\0') {
      count++;
      x++;
   }
   return count;
}

void mystrcopy(char src[], char dest[]) {
    int lensrc = mystrlen(src);
    int lendest = mystrlen(dest);

    if (lensrc > lendest) {
        int i;
        for (i = 0; i <= lensrc; i++) {
            dest[i] = src[i];
        }
        dest[i] = '\0'; // add the null terminator

    } else {
        int count = 0;
        while(*src != '\0') {
            dest[count] = src[count];
            count++;
            src++;
        }
        dest[count] = '\0';
    }
    printf("dest is %s", dest);
}

int main(int argc, char *argv[]) {
   char x[] = "abc";
   char y[] = "defg";
   mystrcopy(x, y);
}