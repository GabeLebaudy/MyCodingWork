#include <stdio.h>
#include <stdlib.h>

void main_head_func(int num_lines, FILE *input) {
	char cur_char;
	int s = 1;

	for (int i = 0; i < num_lines; i++) {
		while ((cur_char = getc(input)) != '\n') {
			if (cur_char == EOF) {
				s = 0;
				break;
			}

			putc(cur_char, stdout);
		}
		if (s) {
			putc('\n', stdout);
		} else {
			break;
		}
	}
}

int main(int argc, char *argv[]) {
	int n = 10;
	FILE *file_input = stdin;

	if (argc == 1) {
		main_head_func(n, file_input);
	}
	
	for (int i = 1; i < argc; i++) {
		if (argv[i][0] == '-') {
			n = atoi(argv[i]) * -1;
			if (argc == 2) {
				main_head_func(n, file_input);
			}
		} else {
			file_input = fopen(argv[i], "r");
			if (file_input == NULL) {
				perror("Error: File does not exist");
				exit(1);
			}
			main_head_func(n, file_input);
			fclose(file_input);
		}
	}

	return 0;
}
