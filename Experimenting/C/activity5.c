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
        dest[i] = '\0';

    } else {
        int count = 0;
        while(*src != '\0') {
            dest[count] = src[0];
            count++;
            src++;
        }
    }
    printf("dest is %s", dest);
}

void mystrcat(char src[], char dest[]) {
    int lensrc = mystrlen(src);
    int lendest = mystrlen(dest);
    int total_length = lensrc + lendest;

    // dest[total_length] = *dest;
    int index_counter = 0;
    for (int i = lendest;i < total_length;i++) {
        dest[i] = src[index_counter];
        index_counter++;
    }
    dest[total_length] = '\0';
    printf("Dest is: %s\n", dest); 
}

int main(int argc, char *argv[]) {
   char x[] = "defgh";
   char y[] = "abc";

   mystrcat(x, y);
}