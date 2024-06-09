#include <sys/stat.h> // stat
#include <stdio.h> // printf
#include <stdbool.h> // bool type

bool file_exists (char *filename) {
    struct stat buffer;
    return (stat (filename, &buffer) == 0);
}

int main(int ac, char **av) {
    if (ac != 2)
        return 1;
    if (file_exists(av[1]))
        printf("%s exists\n", av[1]);
    else
        printf("%s does not exist\n", av[1]);
    return 0;
}
