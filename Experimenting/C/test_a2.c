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

char **split_command(char *command) {
    int cmd_len = strlen(command);
    int word_count = 1;
    char *values[2] = {NULL, NULL};
    int first_len = 0;

    char *space_ind = strchr(command, ' ');

    if (space_ind != NULL) {
        word_count++;
        first_len = space_ind - command;
    } else {
        first_len = cmd_len;
    }

    values[0] = (char *)malloc(first_len + 1);
    strncpy(values[0], command, first_len);
    values[0][first_len] = '\0';

    if (word_count == 2) {
        values[1] = (char *)malloc(cmd_len-first_len);
        strcpy(values[1], space_ind + 1);
    } else {
        values[1] = NULL;
    }


    char** result = malloc((word_count) * sizeof(char*));
    result[0] = values[0];
    result[1] = values[1];

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


int main() {
    char test_command[] = "HW 1";
    char **test_results = split(test_command, ":");

    printf("%s\n", test_results[0]);
    return 0;

    char first_string[] = "9991912292:HW 3:100";
    char **first_items = split(first_string, ":");
    
    char second_string[] = "2145902184:HW 1:45";
    char **second_strings = split(second_string, ":");

    char third_string[] = "5352794201:Lab 1:65";
    char **third_items = split(third_string, ":");

    char fourth_string[] = "9991912292:Lab 1:100";
    char **fourth_items = split(fourth_string, ":");

    char fifth_string[] = "2145902184:Lab 1:82";
    char **fifth_items = split(fifth_string, ":");

    struct LinkedList grade_list = {NULL}; 
    add_node(&grade_list, first_items);
    add_node(&grade_list, second_strings);
    add_node(&grade_list, third_items);
    add_node(&grade_list, fourth_items);
    add_node(&grade_list, fifth_items);

    // print_list(&grade_list);

    // remove_node(&grade_list, "5352794201:Lab 1");

    print_list(&grade_list);

    stats_student(&grade_list, "Lab 1");

    return 0;
}