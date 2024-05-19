#include <stdio.h>
#include <stdlib.h>

int* create(int n) {
    int* arr = (int*) malloc(n * sizeof(int));
    return arr;
}

int* create2(int n) {
    int* arr2 = (int*) calloc(n, sizeof(int));
    return arr2;
}

int* resize(int arr[], int n) {
    int* arr3 = (int*) realloc(arr, n * sizeof(int));
    return arr3;
}

void print(int *p1, int *p2) {
    printf("%d, %d\n%p, %p\n", *p1, *p2, p1, p2);
}

int* square(int *arr, int n) {
    for (int i = 0; i < n; i++) {
        arr[i] = i * i;
    }
    return arr;
}

int* sum(int *z1, int *z2, int *z3, int size1, int size2, int size3) {
    int final_size = size1 + size2 + size3;
    int* arr = (int*) malloc(final_size * sizeof(int));

    int count = 0;
    for (int i = 0;i < size1; i++) {
        arr[count] = z1[i];
        count++;
    }
    for (int j = 0;j < size2; j++){
        arr[count] = z2[j];
        count++;
    }
    for (int k = 0; k < size3; k++) {
        arr[count] = z3[k];
        count++;
    }

    return arr;
}

void swap(char *a, char *b) {
    char temp = *a;
    *a = *b;
    *b = temp;
}

// Function to generate permutations of a string
void permute(char *str, int left_bound, int right_bound) {
    if (left_bound == right_bound) {
        printf("%s\n", str); // Print the permutation
    } else {
        for (int i = left_bound; i <= right_bound; i++) {
            swap((str + left_bound), (str + i));
            permute(str, left_bound + 1, right_bound);
            swap((str + left_bound), (str + i)); // Backtrack
        }
    }
}

int main () {
    int n = 5;
    int *q1_arr = create(n); 
    int *q2_arr = create2(n);
    q1_arr = resize(q1_arr, 3);

    int x = 5;
    int y = 6;
    print(&x, &y);

    int q5[10] = {0};
    square(&q5[0], 10);
    for (int i = 0; i < 10; i++) {
        printf("%d,", q5[i]);
    }
    printf("\n");

    int x1[5] = {0};
    int x2[8] = {0};
    int x3[3] = {0};
    int *dest = sum(&x1[0], &x2[0], &x3[0], 5, 8, 3);
    for (int j = 0; j < 5 + 8 + 3; j++) {
        printf("%d,", dest[j]);
    }

    char q7[] = "abcd";
    permute(q7, 0, 3);
    return 0;
}