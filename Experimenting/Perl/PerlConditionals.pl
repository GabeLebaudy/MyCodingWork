# This file will be used to demonstrate basic perl conditionals like the if statement.

#Modules
use strict;
use warnings;

my $a = 4;
print("This will print\n") if ($a == 4);

$a = 0;
print("This won't print") if $a; # "0", 0, undefined, (), and "" all evaluate to false.

my $b = 10;

if ($b > 5) {
    print("Value of b: $b.\n");
}

# Else Block
if ($a > 5) {
    print("This won't print");
} else {
    print("The value of a is: $a.\n");
}

$a = 10;
$b = 10;

# Else If
if ($a > $b) {
    print("a is greater than b\n");
} elsif ($a == $b) {
    print("a is equal to b\n");
} else {
    print("a is less than b");
}

# Unless statement (Just if statement, but checks if it evaluates to false)

my $c = 5;
unless ($c < 0) {
    print("c is a natural number!\n");
}

$c = 9;
my $d = 10;
unless ($c <= $d) {
    print("c is greater than d.\n");
} elsif ($c < $d) {
    print("c is less than d.\n");
} else {
    print("c is equal to d.\n");
}

# Given Statement (Similar to switch cases)
use v5.10;

my $e = 10;
#given ($e) {
#    when ($e < 0) { print("e is less than 0\n"); }
#    when ($e == 0) { print("e is equal to 0.\n"); }
#    when ($e > 0) { print("e is greater than 0.\n"); }
#}

# Given is pretty useless, just here in extremely rare cases.





