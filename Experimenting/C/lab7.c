#include <stdio.h>
#include <stdlib.h>

int* sort(int *arr, int n) {
    int tmp;
    for (int i = 0; i < n - 1; i++) {
        for (int j = i; j < n; j++) {
            if (arr[i] > arr[j]) {
                tmp = arr[i];
                arr[i] = arr[j];
                arr[j] = tmp;
            }
        }
    }
    return arr;

}

int dotProduct(int *arr1, int *arr2, int len) {
    int dot = 0;
    for (int l = 0; l < len; l++) {
        dot += arr1[l] * arr2[l];
    }

    return dot;
}

int* createStack(int n) {
    int* arr = (int*) malloc(n * sizeof(int));
    return arr;
}

int* insertElement(int p, int n, int maxSize, int *arr) {
    if (n >= maxSize) {
        arr = (int*) realloc(arr, (n + 1) * sizeof(int));
    }
    arr[n] = p;
    return arr;
}

int* removeElement(int *arr, int n) {
    arr = (int*) realloc(arr, (n - 1) * sizeof(int));
    return arr;
}

int top(int *arr, int n) {
    return arr[n - 1];
}

int main() {
    int array[11] = {8,2,95,37,0,53,-7,8,10,103,1};
    sort(&array[0], 11);

    for (int k = 0; k < 11; k++) {
        printf("%d, ", array[k]);
    }
    printf("\n");

    int a1[3] = {1, 3, -5};
    int a2[3] = {4, -2, -1};
    int result = dotProduct(a1, a2, 3);
    printf("%d\n", result);

    int *a3 = createStack(5);
    for (int a = 0; a < 5; a++) {
        a3[a] = a * 3;
        printf("%d, ", a3[a]);
    }
    printf("\n");

    insertElement(15, 5, 5, &a3[0]);
    for (int b = 0; b < 6; b++) {
        printf("%d, ", a3[b]);
    }
    printf("\n");

    removeElement(&a3[0], 6);
    for (int c = 0; c < 6; c++) {
        printf("%d, ", a3[c]);
    }
    printf("\n");

    int top_element = top(&a3[0], 5);
    printf("%d\n", top_element);

    return 0;
}