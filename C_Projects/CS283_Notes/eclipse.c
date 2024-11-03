#include <stdio.h>
#include <stdlib.h>

void check_dims(int *t, int *b, int *l, int *r, int pos, int width) {
	int row, col;

	row = (pos + 1) / width;
	col = (pos + 1) % width;

	if (*t == 0 || *t > row) {
		*t = row;
	}

	if (*l == 0 || *l > col) {
		*l = col;
	}

	if (*r < col) {
		*r = col;
	}

	if (*b < row) {
		*b = row;
	}
}

int main() {
	int height, width;
	int top, bottom, left, right;
	int sun_p_counter;
	int cr, cc;
	unsigned char *img_input;
	unsigned char *p;	

	scanf("P5 %d %d 255", &width, &height);
	
	img_input = malloc(width * height);	
	p = img_input;
	sun_p_counter = 0;
	top = 0;
	bottom = 0;
	right = 0;
	left = 0;
	
	// Loop through all but last few rows to avoid timestamp
	for (int i = 0; i < height * width - width * 20; i++) {
		*p = getchar();

		if (*p > 110) {
			sun_p_counter++;

			if (sun_p_counter >= 2) {
				check_dims(&top, &bottom, &left, &right, i, width);
			}

		} else {
			sun_p_counter = 0;
		}

		*p++;
	}	

	cr = (top + bottom) / 2;
	cc = (left + right) / 2;
	p = img_input;
	
	printf("P5 500 500 255\n");

	for (int j = cr - 250;j < cr + 250;j++) {
		for (int k = cc - 250;k < cc + 250;k++) {
			putc(*(p + j * width + k), stdout);
		}
	}

	return 0;
}


