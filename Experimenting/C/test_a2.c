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

char **find_values(char *s) {
   int s_len = strlen(s);
   char *values[3];
   values[0] = malloc(11);
   values[1] = malloc(21);
   values[2] = malloc(4);

   int char_counter = 0;
   int item = 0;
   for (int i = 0; i < s_len; i++) {
        if (s[i] == ':') {
            values[item][char_counter] = '\0';
            item++;
            char_counter = 0;
        } else {
            if (item == 0) {
                if (char_counter >= 10) {
                    printf("Error: Student ID must be ten digits");
                    exit(1);
                }

                values[item][char_counter] = s[i];
            } else if (item == 1) {
                if (char_counter >= 20) {
                    printf("Error: assignment name must be 20 characters or less.");
                    exit(1);
                }
                values[item][char_counter] = s[i];
            } else {
                if (char_counter >= 3) {
                    printf("Error: Grade must be a 3 digit integer");
                    exit(1);
                }
                values[item][char_counter] = s[i];
            }
        char_counter++;
        }
    }

    values[item][char_counter] = '\0';
    char **result = malloc(3 * sizeof(char *));

    for (int j = 0; j < 3; j++) {
        result[j] = values[j];
    }

    return result;
}

int main() {
    char sample_string[] = "9991912292:HW 3:100";
    char **strings = find_values(sample_string);
    printf("%s,%s,%s\n", strings[0], strings[1], strings[2]);
    
    char second_string[] = "2145902184:HW 1:45";
    char **second_strings = find_values(second_string);

    struct LinkedList grade_list = {NULL}; 
    add_node(&grade_list, strings);
    add_node(&grade_list, second_strings);

    if (grade_list.head == NULL) {
        printf("Grade list head is null");
    } else {
        printf("%s\n", grade_list.head->data.assignmentName); 
    }
}