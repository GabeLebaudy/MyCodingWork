# This file will be used to demonstrate loops in perl.

#Modules
use strict;
use warnings;


# For loops

# Basic example
print("For Loop Example\n");
my @array = (1..10);

for (@array) { # $_ is the default variable of the for loop the "i". It is automatically assigned to the item at the current index of the array.
    print("$_ ");
}

print("\nFor loop with explicit Iterator\n");

# Explicit Loop Iterator
for my $i (@array) { #If $i was declared before this loop, the loop will use i as an iterator, and its value after the loop is done executing will be what it was before executing.
    print($i * 4, " ");
}

print("\nModifying Iterator Example\n");

# Changing the iterator value
my @array_b = (1..5);
for (@array_b) {
    $_ = $_ + 5;
}

print(@array_b);

print("\nC-Style For Loop Example\n");

# C style for loop
for(my $j = 0; $j < 10; $j++) {
    print("J is $j ");
}

print("\nWhile Loop Example\n");

#While Loops

my $count = 10;
while ($count > 0) { #Option to add a "continue" block, but usually there is no need, as it runs after each iteration of the loop, as if it was part of the loop.
    print("$count ");
    $count--;
}

print("\nSingle Line While Loop Example\n");

# Single line loops
my @array_c = ();
$count = 10;
push(@array_c, $count--) while($count > 0);
print(@array_c);

print("\nDo While Example\n");

# Do While (Checks condition after loop, so it always runs at least once)
my $counter = 10;
do {
    print("$counter ");
    $counter -= 2;
} while ($counter > 10);

print("\nUntil Loop Example\n");

# Until loop (Loops until condition is false)

my $loop_counter = 0;
until ($loop_counter > 10) {
    print($loop_counter, " ");
    $loop_counter++;
}

print("\nDo Until Example\n");

# Do Until (Same as do while, but continuing if the condition is false)
my $until_counter = 10;
do {
    print($until_counter, "-> ");
    $until_counter--;
} until($until_counter < 0);

print("\nNext Keyword Example\n");

# Next Keyword (Similar to continue keyword from python)
my $next_counter = 0;
while($next_counter < 10) {
    print($next_counter);
    $next_counter++;
    next if($next_counter == 10);
    print("->")
}

print("\nLast Keyword Example\n");

# Last Keyword (Similar to break keyword from python)
my $last_counter = 5;
while ($last_counter < 15) {
    print("$last_counter->");
    $last_counter++;
    last if($last_counter % 9 == 0);
}
