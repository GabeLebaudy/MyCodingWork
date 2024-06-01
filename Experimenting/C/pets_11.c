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
    struct Node *next;
} 

struct LinkedList{
    struct Node *head;
}

int main() {
    //Initialize Vars
    FILE *input = stdin;

    char *s = NULL;
    size_t nbytes = 0;
    ssize_t nchars;
    int count = 0;
    int size = 1;
    struct LinkedList pet_list; 
    struct Node current_node;

    // Read lines from the input
    while ((nchars = getline(&s, &nbytes, input)) != -1) {
        if (s == NULL) exit(1);

        //clear newline
        s[nchars-1]='\0';
        nchars--;
        
        if (count % 3 == 0) {
            struct Pet temp_pet;
            struct Node temp_node;
        }

        //Ensure input < 16 characters
        if (strlen(s) > 16) {
            printf("Error: Name or species cannot be longer than 16 characters.");
            return 1;
        }

        if (count % 3 == 0) {
            temp_pet->name = s;
        }

        if (count % 3 == 1) {
            temp_pet->age = atoi(s);
        }

        if (count % 3 == 2) {
            temp_pet->species = s;
            temp_node->pet = *temp_pet;

            if (pet_list->head == NULL) {
                pet_list->head = *temp_pet;
            } else {
                current_node->next = *temp_pet;
                current_node = *temp_pet
            }
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
    struct Node head_node;
    struct Node free_node;
    head_node = LinkedList->head;

    while (head_node->next != NULL) {
        printf("%s, %d, %s",  head_node->name, head_node->age, head_node->species);
        free_node = *head_node;
        head_node = head_node->next;
        free_node = NULL;
        free(free_node);
    }

    return 0;
}
