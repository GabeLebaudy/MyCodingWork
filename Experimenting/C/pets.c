#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <errno.h>

struct Pet{
    char name[16]; // max 15 characters (plus room for null terminator)
    int age;
    char species[16];
};

void resize(struct Pet **arr, int n) {
    *arr = (struct Pet*) realloc(arr, n * sizeof(struct Pet));
}

int main() {
    //Initialize Vars
    FILE *input = stdin;

    char *s = NULL;
    size_t nbytes = 0;
    ssize_t nchars;
    int count = 0;
    int size = 1;
    struct Pet *pets = malloc(size * sizeof(struct Pet));

    // Read lines from the input
    while ((nchars = getline(&s, &nbytes, input)) != -1) {
        if (s == NULL) exit(1);

        //clear newline
        s[nchars-1]='\0';
        nchars--;

        //Resize pet array if necessary
        if (size <= count) {
            size *= 2;
            resize(&pets, size);
        }
        if (count % 3 == 0) {
            if (strlen(s) > 16) {
                printf("Error: Name or species cannot be longer than 16 characters.");
                return 1;
            }
            strncpy(pets[count / 3].name, s, 15);
            pets[count / 3].name[15] = '\0';
        }

        if (count % 3 == 1) {

            pets[count / 3].age = atoi(s);
        }

        if (count % 3 == 2) {
            if (strlen(s) > 16) {
                printf("Error: Name or species cannot be longer than 16 characters.");
                return 1;
            }
            strncpy(pets[count / 3].species, s, 15);
            pets[count / 3].species[15] = '\0';
        }
        count++;
    }

    free(s);
    fclose(input);

    if (count % 3 != 0) {
        printf("Error: The final pet is missing information.");
        return 1;
    }

    //Print out pet data
    for (int i = 0; i < count / 3; i++) {
        printf("%s, %d, %s",  pets[i].name, pets[i].age, pets[i].species);
    }

    return 0;
}
