#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/stat.h>

typedef struct Node {
	int *puzzle;
	struct Node *prev, *next;
	int move, num_moves;
}Node;

typedef struct List {
	Node *head, *tail;
}List;

typedef struct HashTable {
	List *buckets;
}HashTable;

int isEmpty(List q) {
	if (q.head == NULL) {
		return 0;
	} else {
		return 1;
	}
}

void enqueue(List *q, Node *add) {
	if(q->head == NULL) {
		q->head = add;
		q->tail = add;
	} else {
		q->tail->next = add;
		q->tail = add;
	}
}

Node *dequeue(List *q) {
	Node *temp;
	temp = q->head;
	if(temp->next != NULL) {
		q->head = temp->next;
	} else {
		q->head = NULL;
		q->tail = NULL;
	}
	return temp;
}

int hashNode(int *board, int k) {
	int i, s, h;

	s = 1;
	h = 0;
	for(i = k * k - 1;i >= 0;i--) {
		h += (s / (k * k)) * board[i];
		s = (s * 31) % 100000;
		if (s < (k * k)) {
			s = k * k;
		}
	}
	h %= 100000;
	//printf("H is %d\n", h);
	return h;
}

int *split_input_info(char *finfo, int *bsize) {
	char *p, *nums;
	int *board;
	int c;

	p = strtok(finfo, "\n");
	c = 1;
	while (p != NULL) {
		if (c == 2) {
			*bsize = atoi(p);
		} else if (c == 4) {
			nums = (char*)malloc(sizeof(p));
			strcpy(nums, p);
		}
		c++;
		p = strtok(NULL, "\n");
	}

	board = (int*)malloc((*bsize * *bsize) * sizeof(int));
	p = strtok(nums, " ");
	c = 0;
	while(p != NULL) {
		board[c] = atoi(p);
		p = strtok(NULL, " ");
		c++;
	}
	return board;
}

int *genSolvedBoard(int k) {
	int *board;
	int i;

	board = (int*)malloc(sizeof(int) * k * k);
	for(i = 0; i < k * k;i++) {
		board[i] = i + 1;
	}
	board[i - 1] = 0;
	return board;
}

int boardExists(List *bucket, int *board, int k) {
	Node *tmp;
	
	if(bucket->head == NULL) {
		return 0;
	}
	tmp = bucket->head;
	while (tmp != NULL) {
		if (memcmp(tmp->puzzle, board, k * k * sizeof(int)) == 0) {
			return 1;
		}
		tmp = tmp->next;
	}
	return 0;
}

int checkNode(Node *n, List *que, int *solved, int k, HashTable *table) {
	int row, col, ind, i, tmp;
	Node *left, *right, *top, *bottom;
	int *temp_board;
	
	//1. Check if it's solved
	if (memcmp(solved, n->puzzle, k * k * sizeof(int)) == 0) {
		return 1;
	}

	//2. Check what moves are possible based off of open square position
	for(i = 0;i < k * k;i++) {
		if(n->puzzle[i] == 0) {
			ind = i;
			break;
		}
	}
	row = ind / 3;
	col = ind % 3;
	temp_board = (int*)malloc(k * k * sizeof(int));
	//Item can be moved down into square
	if (row > 0) {
		// printf("Row above\n");
		// fflush(stdout);
		memcpy(temp_board, n->puzzle, k * k * sizeof(int));
		tmp = temp_board[ind - k];
		temp_board[ind - k] = temp_board[ind];
		temp_board[ind] = tmp;
		if(boardExists(&table->buckets[hashNode(temp_board, k)], temp_board, k) == 0) {
			top = (Node*)malloc(sizeof(Node*));
			top->puzzle = (int*)malloc(k * k * sizeof(int));
			memcpy(top->puzzle, temp_board, k * k * sizeof(int));
			top->prev = n;
			top->num_moves = n->num_moves + 1;
			top->move = temp_board[ind];
			enqueue(que, top);
		}
	}

	//Item can be moved up into square
	if (row < k - 1) {
		// printf("Row below.\n");
		// fflush(stdout);
		memcpy(temp_board, n->puzzle, k * k * sizeof(int));
		tmp = temp_board[ind + k];
		temp_board[ind + k] = temp_board[ind];
		temp_board[ind] = tmp;
		if(boardExists(&table->buckets[hashNode(temp_board, k)], temp_board, k) == 0) {
			bottom = (Node*)malloc(sizeof(Node*));
			bottom->puzzle = (int*)malloc(k * k * sizeof(int));
			memcpy(bottom->puzzle, temp_board, k * k * sizeof(int));
			bottom->prev = n;
			bottom->num_moves = n->num_moves + 1;
			bottom->move = temp_board[ind];
			enqueue(que, bottom);
		}
	}

	//Item can be moved in from left
	if (col > 0) {
		// printf("Col to the left.\n");
		// fflush(stdout);
		memcpy(temp_board, n->puzzle, k * k * sizeof(int));
		tmp = temp_board[ind - 1];
		temp_board[ind - 1] = temp_board[ind];
		temp_board[ind] = tmp;
		if(boardExists(&table->buckets[hashNode(temp_board, k)], temp_board, k) == 0) {
			left = (Node*)malloc(sizeof(Node*));
			left->puzzle = (int*)malloc(k * k * sizeof(int));
			memcpy(left->puzzle, temp_board, k * k * sizeof(int));
			left->prev = n;
			left->num_moves = n->num_moves + 1;
			left->move = temp_board[ind];
			enqueue(que, left);
		}
	}

	//Item can be moved in from right
	if (col < k - 1) {
		// printf("Col to the right.\n");
		// fflush(stdout);
		memcpy(temp_board, n->puzzle, k * k * sizeof(int));
		tmp = temp_board[ind + 1];
		temp_board[ind + 1] = temp_board[ind];
		temp_board[ind] = tmp;
		if(boardExists(&table->buckets[hashNode(temp_board, k)], temp_board, k) == 0) {
			right = (Node*)malloc(sizeof(Node*));
			right->puzzle = (int*)malloc(k * k * sizeof(int));
			memcpy(right->puzzle, temp_board, k * k * sizeof(int));
			right->prev = n;
			right->num_moves = n->num_moves + 1;
			right->move = temp_board[ind];
			enqueue(que, right);
		}
	}
	return 0;
}

int main(int argc, char **argv) {
	FILE *fp_in,*fp_out;
	struct stat fi;
	int infsize, k, h, i, solved;
	int *init_board, *solved_board;
	char *input_info;
	HashTable table;
	List q;
	Node *root, *cur;
	
	if (stat(argv[1], &fi) != -1) {
		infsize = fi.st_size;
	} else {
		fprintf(stderr, "Invalid input file.\n");
		return 1;
	}
	
	fp_in = fopen(argv[1], "r");
	if (fp_in == NULL){
		printf("Could not open a file.\n");
		return -1;
	}

	input_info = (char*)malloc(infsize + 1);
	fread(input_info, 1,  infsize, fp_in);
	input_info[infsize] = 0;
	fclose(fp_in);
	init_board = split_input_info(input_info, &k);
	solved_board = genSolvedBoard(k);

	root = (Node*)malloc(sizeof(Node*));
	root->num_moves = 0;
	root->puzzle = (int*)malloc(k * k * sizeof(int));
	memcpy(root->puzzle, init_board, k * k * sizeof(int));
	table.buckets = (List*)malloc(sizeof(List) * 100000);

	enqueue(&q, root);
	h = hashNode(root->puzzle, k);
	enqueue(&table.buckets[h], root);

	cur = root;
	solved = 0;
	while(q.head != NULL) {
		if (checkNode(cur, &q, solved_board, k, &table)) {
			solved = 1;
			break;
		}
		cur = dequeue(&q);
	}
	
	return 0;
	fp_out = fopen(argv[2], "w");
	if (fp_out == NULL){
		printf("Could not open a file.\n");
		return -1;
	}

	//once you are done, you can use the code similar to the one below to print the output into file
	//if the puzzle is NOT solvable use something as follows
	fprintf(fp_out, "#moves\n");
	fprintf(fp_out, "no solution\n");
	
	//if it is solvable, then use something as follows:
	fprintf(fp_out, "#moves\n");
	//probably within a loop, or however you stored proper moves, print them one by one by leaving a space between moves, as below
	// for(int i=0;i<numberOfMoves;i++)
	// 	fprintf(fp_out, "%d ", move[i]);

	// fclose(fp_out);

	return 0;

}
