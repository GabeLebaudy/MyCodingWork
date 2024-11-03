#include <stdio.h>

void find_pairs(int *arr, int size) {
    int q, p, r, t, diff, temp;
    int do_cont = 1;
    for(int i = 0;i < size;i++) {
        q = arr[i];
        r = arr[i + 1];
        diff = q-r;
        for (int j = i + 2;j < size;j++) {
            p = arr[j];
            t = arr[j + 1];
            if (diff == p - t) {
                temp = p;
                p = t;
                t = temp;
                do_cont = 0;
                break;
            } else if (diff * -1 == p - t) {
                do_cont = 0;
                break;
            }
        }
        if (do_cont == 0) {
            break;
        }
    }
    printf("%d, %d, %d, %d\n", p, q, r, t);
}

int main() {
    int arr[20] = {1, 7, 3, 1000, 5, 2056, 7, 145, 287, 14, 21, 12, 45, 14, 15, 16, 17, 18, 19};
    int size = sizeof(arr) / sizeof(int);
    find_pairs(arr, size);
}