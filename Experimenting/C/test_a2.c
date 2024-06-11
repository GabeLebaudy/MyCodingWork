#include <stdio.h>
#include <stdlib.h>
#include <sys/stat.h>
#include <stdbool.h>
#include <errno.h>
#include <string.h>

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
    Node *temp_node = grades_list.head;
    int did_find = 0;
    while (temp_node != NULL) {
        if (strcpm(temp_node->data.studentId, values[0]) && strcmp(temp_node->data.assignmentName, values[1])) {
            did_find = 1;
            break;
        } else {
            temp_node = temp_node->next;
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

void stats_student(struct LinkedList *grades_list, char *studentID) {

}

char** split(const char* str, const char* delim) {
    char* str_copy = strdup(str);

    int token_count = 0;
    char* tmp = str_copy;
    char* token = strtok(tmp, delim);
    while (token != NULL) {
        token_count++;
        token = strtok(NULL, delim);
    }

    char** result = malloc((token_count + 1) * sizeof(char*));

    // Reset the string and tokenize again to fill the result array
    strcpy(str_copy, str);
    token = strtok(str_copy, delim);
    int index = 0;
    while (token != NULL) {
        result[index] = strdup(token);
        index++;
        token = strtok(NULL, delim);
    }

    // Null-terminate the array
    result[index] = NULL;

    // Free the copied string
    free(str_copy);

    return result;
}

int main() {
    char sample_string[] = "9991912292:HW 3:100";
    char **strings = split(sample_string, ":");
    printf("%s,%s,%s\n", strings[0], strings[1], strings[2]);
    
    char second_string[] = "2145902184:HW 1:45";
    char **second_strings = split(second_string, ":");

    struct LinkedList grade_list = {NULL}; 
    add_node(&grade_list, strings);
    add_node(&grade_list, second_strings);

    if (grade_list.head == NULL) {
        printf("Grade list head is null");
    } else {
        printf("%s\n", grade_list.head->next->data.assignmentName); 
    }

    return 0;
}