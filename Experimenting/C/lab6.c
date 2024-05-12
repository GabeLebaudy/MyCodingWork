#include <stdio.h>

int binSearch(int arr[], int n, int target) {
    int left = 0;
    int mid = n / 2;
    while (left <= n) {
        mid = (left + n) / 2;
        if (arr[mid] == target) {
            return mid;
        } 
        if (arr[mid] < target) {
            left = mid + 1;
        } else {
            n = mid - 1;
        }
    }
    return -1;
}

void arrStats(double arr[], int size, double *mean, double *max, double *min) {
    double total = 0;
    *max = arr[0];
    *min = arr[0];
    for (int i = 0; i < size; i++) {
        if (arr[i] > *max) {
            *max = arr[i];
        }
        if (arr[i] < *min) {
            *min = arr[i];
        }
        total += arr[i];
    }
    *mean = total / size;
}

int* arrFind(int arr[], int length, int target) {
    int count = 0;
    int *point = arr;
    while (count < length) {
        if (*point == target) {
            return point;
        }
        count++;
        point++;
    }
    return NULL;
} 

void capatilize(char *x) {
    while (*x != '\0') {
        if (*x >= 'a' && *x <= 'z') {
            *x -= 32;
        }
        x++;
    }
}

int main () {
    // Q1
    int sample[] = {1, 2, 3, 4, 5};
    int n = sizeof(sample) / sizeof(int);
    int ind = binSearch(sample, n, 10);
    //printf("%d\n", ind);

    // Q2
    double arrStat[] = {1.4, 2.685, 5.8, -5.72, 10.87};
    int sizeArr = sizeof(arrStat) / sizeof(double);
    double mean = 0;
    double max = 0;
    double min = 0;
    arrStats(arrStat, sizeArr, &mean, &max, &min);
    // printf("%.2f, %.2f, %.2f\n", mean, max, min);

    // Q3
    int q3Arr[] = {3, 5, 7, 9, 11};
    int sizeQ3 = sizeof(q3Arr) / sizeof(int);
    int q3Target = 7;
    int *q3Result = arrFind(q3Arr, sizeQ3, q3Target);
    //printf("%d\n", *q3Result);

    // Q4
    char q4Str[] = "SampleWoRd342980&(&*())";
    capatilize(q4Str);
    // printf("%s\n", q4Str);

    return 0;
}