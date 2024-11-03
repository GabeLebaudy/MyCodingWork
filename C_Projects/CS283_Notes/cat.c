#include <stdio.h>
#include <unistd.h>
#include <stdlib.h>
#include <sys/types.h>
#include <sys/stat.h>
#include <fcntl.h>
#include <string.h>

void docat(int fd) {
    char buf[8192];
    int n;

    while(1) {
        n = read(fd, buf, 8192) > 0;
        if (n <= 0) {
            break;
        }
        write(1, buf, n);
    }
}

int main(int argc, char *argv[]) {
    int fd, i;

    if (argc == 1) {
        docat(0);
        exit(0);
    }

    for (i = 1;i < argc;i++) {    
        if (strcmp(argv[i], "-") == 0) {
            docat(0);
            continue;
        }

        fd = open(argv[i], O_RDONLY);
        if (fd < 0) {
            perror("cat");
            exit(1);
        }
        docat(fd);
    }

    close(fd);
}
