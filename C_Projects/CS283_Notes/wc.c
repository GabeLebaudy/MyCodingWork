#include <stdio.h>

//This file is an example of the wc command which counts, number of lines, words, and/or characters in a file.

void dowc(FILE *fp) {
    int n_lines, n_words, n_chars;
    int c;
    int in_word;

    n_lines = 0;
    n_words = 0;
    n_chars = 0;

    while(1) {
        c = getc(fp);
        if(c == EOF) {
            break;
        }
        if(c == '\n') {
            n_lines++;
        }
        ++n_chars;
        if (in_word) {
            if (c == ' ' || c == '\t' || c == '\n') {
                in_word = 0;
            }
        } else {
            if (c != ' ' && c != '\t' && c != '\n') {
                in_word = 1;
                ++n_words;
            }
        }
    }
    printf("%d\t%d\t%d\n", n_lines, n_words, n_chars);
}

int main(int argc, char *argv[]) {
    FILE *fp;
    fp = stdin;
    
    if (argc > 1) {
        fp = fopen(argv[1], "r");
    }
    
    dowc(fp);
}

