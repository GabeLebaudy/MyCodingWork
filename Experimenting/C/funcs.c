#include <stdio.h>

int find(int x[], int n, int target) {
   for (int i = 0; i < n; i++) {
      if (x[i] == target) {
         return i;
      }
   }
   return -1;
}

void uppercase(char s[]) {
   while(*s != '\0') {
      if ('a' <= s[0] && s[0] <= 'z') {
         s[0] = s[0] - 32;
      }
      s++;
   }
}

void int2str(int x, char s[]) {
   int count = 0;
   while (x > 0) {
      int digit = x % 10;
      s[count] = (digit + '0');
      x = x / 10;
      count++;
   }
   int i = 0;
   count--;
   while (i < count) {
      char temp_char = s[i];
      s[i] = s[count];
      s[count] = temp_char;
      count--;
      i++;
   }
}