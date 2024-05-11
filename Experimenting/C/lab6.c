#include <stdio.h>

void trimArr(int arr[], int start, int stop, int final[]) {
    for (int i = start; i < stop; i++) {
        final[i - start] = arr[i];
    }
}

int binSearch(int arr[], int n, int target) {
    return 0;
}
int main () {
    int sample[] = {1, 2, 3, 4, 5};
    int small[1]; 
    trimArr(sample, 2, 3, sample);
    int n = sizeof(small) / sizeof(int);
    for (int i = 0; i < n; i++) {
        printf("%d, ", small[i]);
    }
    return 0;
}