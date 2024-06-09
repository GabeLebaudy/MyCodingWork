#include <stdio.h>
#include <stdlib.h>
#include <sys/stat.h>
#include <stdbool.h>

bool file_exists (char *filename) {
    struct stat buffer;
    return (stat (filename, &buffer) == 0);
}

struct GradeEntry {
    char studentId[11]; // 10 digit ID with space for \0
    char assignmentName[21]; // max 20 char name with space for \0
    unsigned short grade; // use format specifer %hu to print
};

typedef struct Node Node;
struct Node{
    struct GradeEntry data;
    Node *next;
};

struct LinkedList{
    Node *head;
};


int main(int ac, char **av) {
    if (ac != 2) {
        printf("Error: File argument must be provided.");
        return 1;
    }

    if (!file_exists(av[1])) {
        return 1;
    }
    
    FILE *input = open(*av[1]);
    char *s = NULL;
    size_t nbytes = 0;
    ssize_t nchars;
    int line_count = 0;
    int line_size = 0;
    struct LinkedList pet_list = {NULL}; 
    Node *temp_node;
    struct GradeEntry temp_entry;

    while ((nchars = getline(&s, &nbytes, input)) != -1) {
        if (s == NULL) exit(1);

        //clear newline
        s[nchars-1]='\0';
        nchars--;
    }

    return 0;
}
