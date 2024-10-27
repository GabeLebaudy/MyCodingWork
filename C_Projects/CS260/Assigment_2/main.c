#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>

#define BUFSIZE 256

typedef struct Item{
  char *word;
  int weight;
}Item;

typedef struct WordStorage {
    Item *words;
    int size;
    int capacity;
} WordStorage;

typedef struct HashMap {
    WordStorage *buckets[27];
} HashMap;

void initHashMap(HashMap *map) {
    for (int i = 0;i < 27;i++) {
        map->buckets[i] = (WordStorage*)malloc(sizeof(WordStorage));
        map->buckets[i]->size = 0;
        map->buckets[i]->capacity = 2;
        map->buckets[i]->words = (Item*)malloc(sizeof(Item) * 2);
    }
}

void doubleStorageCapacity(WordStorage *storage) {
    storage->capacity *= 2;
    storage->words = (Item*)realloc(storage->words, storage->capacity * sizeof(Item));
}

void printBucket(WordStorage *storage) {
    for (int i = 0; i < storage->size;i++) {
        printf("%s->", storage->words[i].word);
    }
    printf("\n");
}

void insertItem(WordStorage *storage, Item *item) {
    int ins_ind = storage->size;
    int is_dupe = 1;

    if (storage->size >= storage->capacity) {
        doubleStorageCapacity(storage);
    }

    for (int i = 0;i < storage->size;i++) {
        if (strcmp(storage->words[i].word, item->word) == 0) {
            //Repeat word, exit
            is_dupe = 0;
            printf("Duplicate word: %s, %s\n", storage->words[i].word, item->word);
            break;
        }

        if (strcmp(storage->words[i].word, item->word) > 0) {
            ins_ind = i;
            break;
        }
    }

    if (is_dupe) {
        for (int j = storage->size - 1;j >= ins_ind;j--) {
             storage->words[j + 1] = storage->words[j];
        }

        storage->words[ins_ind] = *item;
        storage->size++;
    }
}

void findIndices(int *l, int *r, int pos, char letter, WordStorage *storage) {
    int mid;
    char pivot;
    
    while (*l <= *r) {
        mid = (*l + *r) / 2;
        while (strlen(storage->words[mid].word) <= pos) {
            mid++;
            if (mid > *r) {
                break;
            }
        }
        pivot = storage->words[mid].word[pos];
        if (pivot < letter) {
            *l = mid + 1;
        } else if (pivot > letter) {
            *r = mid - 1;
        } else {
            break;
        }
    }

    *l = mid;
    *r = mid;
    while (*l > 0) {
        if (strlen(storage->words[*l].word) > pos) {
            if (storage->words[*l].word[pos] != letter) {
                (*l)++;
                break;
            }
        }
        (*l)--;
    }
    
    while (*r < storage->size) {
        if (strlen(storage->words[*r].word) > pos) {
            if (storage->words[*r].word[pos] != letter) {
                (*r)--;
                break;
            }
        }
        (*r)++;
    }
}

void findMatches(WordStorage *dict, WordStorage *out, char *qword) {
    int left = 0;
    int right = dict->size - 1;
    int pos = 1;
    //printf("%s\n", qword);

    while (pos < strlen(qword)) {
        findIndices(&left, &right, pos, qword[pos], dict);
        if (left > right) {
            break;
        }
        pos++;
    }

    out->size = 0;
    if (left < right) {
        out->words = (Item*)malloc((right - left) * sizeof(Item));
        out->capacity = right - left;

        for (int i = 0; i < (right - left);i++) {
            out->words[i].word = (char*)malloc(strlen(dict->words[left + i].word));
            strcpy(out->words[i].word, dict->words[left + i].word);
            out->words[i].weight = dict->words[left + i].weight;
            out->size++;
        }
    }
        
}  

void printTopTen(WordStorage *storage) {
    int cur_max;
    int max_pos;
    Item temp_item;
    int n;

    if (storage->size > 10) {
        n = 10;
    } else {
        n = storage->size;
    }

    for (int i = 0;i < n; i++) {
        cur_max = 0;
        max_pos = i;
        for (int j = i;j < storage->size;j++) {
            if (storage->words[j].weight > cur_max) {
                cur_max = storage->words[j].weight;
                max_pos = j;
            }
        }
        if (i != max_pos) {
            temp_item = storage->words[i];
            storage->words[i] = storage->words[max_pos];
            storage->words[max_pos] = temp_item;
        }

        printf("%s %d\n", storage->words[i].word, storage->words[i].weight);
    }
}

int main(int argc, char **argv) {
    char *dictionaryFilePath = argv[1]; //this keeps the path to dictionary file
    char *queryFilePath = argv[2]; //this keeps the path to the file that keeps a list of query wrods, 1 query per line
    int wordCount=0; //this variable will keep a count of words in the dictionary, telling us how much memory to allocate
    int queryCount=0; //this variable will keep a count of queries in the query file, telling us how much memory to allocate for the query words
    
    ////////////////////////////////////////////////////////////////////////
    ///////////////////////// read dictionary file /////////////////////////
    ////////////////////////////////////////////////////////////////////////
    FILE *fp = fopen(dictionaryFilePath, "r");
    char *line = NULL; //variable to be used for line counting
    size_t lineBuffSize = 0; //variable to be used for line counting
    ssize_t lineSize; //variable to be used for line counting
    
    //check if the file is accessible, just to make sure...
    if(fp == NULL){
        fprintf(stderr, "Error opening file:%s\n", dictionaryFilePath);
        return -1;
    }

    //First, let's count number of lines. This will help us know how much memory to allocate
    while((lineSize = getline(&line,&lineBuffSize,fp)) !=-1)
    {
        wordCount++;
    }

    //Printing wordCount for debugging purposes. You can remove this part from your submission.
    //printf("%d\n",wordCount);
    
    /////////////////PAY ATTENTION HERE/////////////////
    //This might be a good place to allocate memory for your data structure, by the size of "wordCount"
    ////////////////////////////////////////////////////
    HashMap all_word_items;
    initHashMap(&all_word_items);

    //Read the file once more, this time to fill in the data into memory
    fseek(fp, 0, SEEK_SET);// rewind to the beginning of the file, before reading it line by line.
    char word[BUFSIZE]; //to be used for reading lines in the loop below
    int weight;
    Item *temp_item;
    int bucket;
    for(int i = 0; i < wordCount; i++)
    {
        fscanf(fp, "%s %d\n",word,&weight);
        //Let's print them to the screen to make sure we can read input, for debugging purposes. You can remove this part from your submission.
        //printf("Adding: %s %d\n",word,weight);

        /////////////////PAY ATTENTION HERE/////////////////
        //This might be a good place to store the dictionary words into your data structure
        ////////////////////////////////////////////////////
        temp_item = (Item *)malloc(sizeof(Item));
        temp_item->word = malloc(sizeof(word));
        strcpy(temp_item->word, word);
        temp_item->weight = weight;
        bucket = word[0] - 97;
        if (bucket > 25 || bucket < 0) {
            bucket = 26;
        }

        insertItem(all_word_items.buckets[bucket], temp_item);
    }
    //close the input file
    fclose(fp);

    //printBucket(all_word_items.buckets[24]);

    ////////////////////////////////////////////////////////////////////////
    ///////////////////////// read query list file /////////////////////////
    ////////////////////////////////////////////////////////////////////////
    fp = fopen(queryFilePath, "r");
        
    //check if the file is accessible, just to make sure...
    if(fp == NULL){
        fprintf(stderr, "Error opening file:%s\n",queryFilePath);
        return -1;
    }

    //First, let's count number of queries. This will help us know how much memory to allocate
    while((lineSize = getline(&line,&lineBuffSize,fp)) !=-1)
    {
        queryCount++;
    }
    free(line); //getline internally allocates memory, so we need to free it here so as not to leak memory!!

    //Printing line count for debugging purposes. You can remove this part from your submission.
    //printf("%d\n",queryCount);

    /////////////////PAY ATTENTION HERE/////////////////
    //This might be a good place to allocate memory for storing query words, by the size of "queryCount"
    ////////////////////////////////////////////////////

    fseek(fp, 0, SEEK_SET);// rewind to the beginning of the file, before reading it line by line.
    char **query_words;
    query_words = (char**)malloc(queryCount * sizeof(char*));
    for(int i = 0; i < queryCount; i++)
    {
        fscanf(fp, "%s\n",word);
        //Let's print them to the screen to make sure we can read input, for debugging purposes. You can remove this part from your submission.
        //printf("%s %d\n",word);
        
        /////////////////PAY ATTENTION HERE/////////////////
        //This might be a good place to store the query words in a list like data structure
        ////////////////////////////////////////////////////   
        query_words[i] = (char*)malloc(sizeof(word));
        strcpy(query_words[i], word);
    }
    //close the input file
    fclose(fp);

    ////////////////////////////////////////////////////////////////////////
    ///////////////////////// reading input is done ////////////////////////
    ////////////////////////////////////////////////////////////////////////
    WordStorage *output;
    for (int i = 0;i < queryCount;i++) {
        output = (WordStorage*)malloc(sizeof(WordStorage));
        
        bucket = query_words[i][0] - 97;
        if (bucket > 25 || bucket < 0) {
            bucket = 26;
        }

        printf("Query word:%s\n", query_words[i]);
        findMatches(all_word_items.buckets[bucket], output, query_words[i]);

        if (output->size <= 0) {
            printf("No suggestion!\n");
        } else {
            printTopTen(output);
        }
    }
    //Now it is your turn to do the magic!!!
    //do search/sort/print, whatever you think you need to do to satisfy the requirements of the assignment!
    //loop through the query words and list suggestions for each query word if there are any
    //don't forget to free the memory before you quit the program!
    
    //OUTPUT SPECS:
    // use the following if no word to suggest: printf("No suggestion!\n");
    // use the following to print a single line of outputs (assuming that the word and weight are stored in variables named word and weight, respectively): 
    // printf("%s %d\n",word,weight);
    // if there are more than 10 outputs to print, you should print the top 10 weighted outputs.
    
    return 0;
}
