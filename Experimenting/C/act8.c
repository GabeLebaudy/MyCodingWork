#include <stdio.h>
#include <stdlib.h>
#include <errno.h>
#include <string.h>

struct Match{
    int lineNum;
};


FILE *open(char *filename) {
    FILE *file = fopen(filename, "r");
    if (file == NULL) {
        int error = errno;
        if (error == ENOENT) {
            fprintf(stderr, "File '%s' does not exist\n", filename);
        }
        else if (error == EACCES) {
            fprintf(stderr, "Permission denied for file '%s'\n", filename);
        } else {
            fprintf(stderr, "Something went wrong when opening file '%s'\n", filename);
        }
        exit(1);
    }
    return file;
}

int main(int argc, char *argv[]) {
    //number of arguments
    if (argc < 2 || argc > 3) {
        printf("Only 3 arguments accepted");
        exit(1);
    }

    //assign pattern
    char *pattern = argv[1];
    FILE *input;

    //if 3 arguments, assign filename, open file, else read from stdin
    if (argc == 3) {
        char *filename = argv[2];
        input = open(filename);
    } else {
        input = stdin;
    }

    char *s = NULL;
    size_t nbytes = 0;
    ssize_t nchars;
    int lineNum = 0;
    int matchCount = 0;
    struct Match matches[99999];

    // Read lines from the input
    while ((nchars = getline(&s, &nbytes, input)) != -1) {
        if (s == NULL) exit(1);

        //increment
        lineNum++;

        //clear newline
        s[nchars-1]='\0';
        nchars--;

        //Use strcmp from sting.h to check the pattern and assign it to a struct
        if (strcmp(s, pattern) == 0) {
            matches[matchCount].lineNum = lineNum;
            matchCount++;
        }
    }

    //if matchcount greater than 0, print the matches
    if (matchCount > 0) {
        printf("Here are all matches:\n");
        for (int i = 0; i < matchCount; i++) {
            printf("%d\n", matches[i].lineNum);
        }
    } else {
        printf("No matches found\n");
    }

    free(s);
    fclose(input);

    return 0;
}

