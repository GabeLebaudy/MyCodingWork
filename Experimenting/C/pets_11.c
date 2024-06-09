#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <errno.h>

struct Pet{
    char name[16]; // max 15 characters (plus room for null terminator)
    int age;
    char species[16];
};

typedef struct Node Node;
struct Node{
    struct Pet pet;
    Node *next;
};

struct LinkedList{
    Node *head;
};

int main() {
    //Initialize Vars
    FILE *input = stdin;

    char *s = NULL;
    size_t nbytes = 0;
    ssize_t nchars;
    int count = 0;
    int size = 1;
    struct LinkedList pet_list = {NULL}; 
    Node *current_node = NULL;
    Node *temp_node;
    struct Pet temp_pet;

    // Read lines from the input
    while ((nchars = getline(&s, &nbytes, input)) != -1) {
        if (s == NULL) exit(1);

        //clear newline
        s[nchars-1]='\0';
        nchars--;
        
        //Ensure input < 16 characters
        if (strlen(s) > 16) {
            printf("Error: Name or species cannot be longer than 16 characters.");
            return 1;
        }

        if (count % 3 == 0) {
            strncpy(temp_pet.name, s, 15);
            temp_pet.name[15] = '\0';
        }

        if (count % 3 == 1) {
            temp_pet.age = atoi(s);
        }

        if (count % 3 == 2) {
            strncpy(temp_pet.species, s, 15);
            temp_pet.species[15] = '\0';

            temp_node = (Node *)malloc(sizeof(Node));
            temp_node->pet = temp_pet;

            if (pet_list.head == NULL) {
                pet_list.head = temp_node;
            } else {
                current_node->next = temp_node;
            }
            current_node = temp_node;
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
    Node *head_node;
    Node *free_node;
    head_node = pet_list.head;

    while (head_node != NULL) {
        printf("%s, %d, %s",  head_node->pet.name, head_node->pet.age, head_node->pet.species);
        free_node = head_node;
        head_node = head_node->next;
        free(free_node);
    }

    return 0;
}
