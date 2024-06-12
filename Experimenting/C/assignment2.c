#include <stdio.h>
#include <stdlib.h>
#include <sys/stat.h>
#include <stdbool.h>
#include <errno.h>
#include <string.h>


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

char** split(const char* str, const char* delim) {
    char* str_copy = strdup(str);
    int token_count = 0;
    char* tmp = str_copy;
    char* token = strtok(tmp, delim);

    while (token != NULL) {
        token_count++;
        token = strtok(NULL, delim);
    }

    char** result = malloc((token_count) * sizeof(char*));
    strcpy(str_copy, str);
    token = strtok(str_copy, delim);
    int index = 0;

    while (token != NULL) {
        result[index] = strdup(token);
        index++;
        token = strtok(NULL, delim);
    }

    free(str_copy);
    return result;
}

void add_node(struct LinkedList *grades_list, char **values) {
    Node *temp_node = (Node *)malloc(sizeof(Node));
    
    strncpy(temp_node->data.studentId, values[0], 10);
    temp_node->data.studentId[10] = '\0';

    strncpy(temp_node->data.assignmentName, values[1], 20);
    temp_node->data.assignmentName[20] = '\0';

    temp_node->data.grade = atoi(values[2]);

    Node *current_node = grades_list->head;
    if (current_node == NULL) {
        grades_list->head = temp_node;
    } else {
        while (current_node->next != NULL) {
            current_node = current_node->next;
        }
        current_node->next = temp_node;
    }

}

void remove_node(struct LinkedList *grades_list, char *info) {
    Node *temp_node = grades_list->head;
    int did_find = 0;

    char **remove_items = split(info, ":");

    while (temp_node!= NULL) {
        if (strcmp(temp_node->data.studentId, remove_items[0]) == 0 && strcmp(temp_node->data.assignmentName, remove_items[1]) == 0) {
            did_find = 1;
            break;
        } else {
            temp_node = temp_node->next;
        }
    }

    if (did_find == 0) {
        printf("Student ID or assignment name is invalid.\n");
    } else {
        //Cases: Node is head. Node is at the end, Node is somewhere in the middle
        if (temp_node == grades_list->head) {
            if (temp_node->next != NULL) {
                grades_list->head = temp_node->next;
            }
            free(temp_node);  
        } else if (temp_node->next == NULL) {
            Node *prior_node = grades_list->head;
            while (prior_node->next != temp_node) {
                prior_node = prior_node->next;
            }
            prior_node->next = NULL;
            free(temp_node);
        } else {
            Node *prior_node = grades_list->head;
            while (prior_node->next != temp_node) {
                prior_node = prior_node->next;
            }
            prior_node->next = temp_node->next;
            free(temp_node);
        }
    }
    
}

void print_list(struct LinkedList *grades_list) {
    printf("Student ID | Assignment Name     | Grade\n------------------------------------------\n");

    Node *temp_node = grades_list->head;
    while (temp_node != NULL) {
        printf("%10s | %-20s| %-3hu\n", temp_node->data.studentId, temp_node->data.assignmentName, temp_node->data.grade);
        temp_node = temp_node->next;
    }
}

void stats_student(struct LinkedList *grades_list, char *assignmentName) {
    Node *temp_node = grades_list->head;
    int min = 100;
    int max = 0;
    int total = 0;
    int count = 0;
    while (temp_node != NULL) {
        if (strcmp(assignmentName, temp_node->data.assignmentName) == 0) {
            total += temp_node->data.grade;
            if (temp_node->data.grade > max) {
                max = temp_node->data.grade;
            }

            if (temp_node->data.grade < min) {
                min = temp_node->data.grade;
            }
            count++;
        }
        temp_node = temp_node->next;
    }
    float avg = (float)total / count;

    printf("Min: %d\nMax: %d\nMean: %.2f\n", min, max, avg);
}

int main(int ac, char **av) {
    if (ac != 2) {
        printf("Error: File argument must be provided.");
        return 1;
    }

    if (!file_exists(av[1])) {
        return 1;
    }
    
    FILE *input = fopen(av[1], "r");
    char *s = NULL;
    size_t nbytes = 0;
    ssize_t nchars;
    struct LinkedList grade_list = {NULL}; 

    while ((nchars = getline(&s, &nbytes, input)) != -1) {
        if (s == NULL) exit(1);

        //clear newline
        s[nchars-1]='\0';
        nchars--;
    }

    return 0;
}
