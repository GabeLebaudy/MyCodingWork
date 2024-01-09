# This file will be for learning the basics of perl.

#Modules
use strict;
use warnings;

# Basic Variables
my $sample_string = "Example String";
my $sample_integer = 20;

print("Value of example string: $sample_string. Value of sample integer: $sample_integer.\n");

# Operators
my $a = 4;
my $b = 2;

# How you define a block of code: (Has it's own layer of scope).
{
    print("The value of a + b: ", $a + $b, "\n"); # Note, comma's do not act like they do in python. They do not add a space, but instead act like the '+' operator
    print("The value of a - b: ", $a - $b, "\n");
    print("The value of a x b: ". $a * $b, "\n");
    print("The value of a / b: ", $a / $b, "\n");
    print("a to the power of b: ", $a ** $b, "\n");
    print("The value of a modulus b: ", $a % $b, "\n");
}

# Comparison Operators
# == Equal to
# != Not equal to
# < less than
# > greater than
# <= less than or equal to
# >= greater than or equal to
# <=> spaceship: Returns 1 if the left variable is greater than the right, 0 if they are equal, and -1 if the left variable is less than the right.

# String Comparison Operators
# eq Equal to
# ne Not equal to
# lt Less than
# gt Greater than
# le Less than or equal to
# ge Greater than or equal to
# cmp Spaceship/comparison

# String concatenation operations
print("This is " . "The concatenation operator." . "\n");
print("This is the repetition multiplier.\n" x 2);

# Chomp Operator
my $chomp_var = "Chomp gets rid of the last character in a string!\n";
print($chomp_var);
chomp($chomp_var);
print("After chomp: $chomp_var\n"); # A little difficult to spot because a newline character is added after it is just chomped.

# Numbers

my $c = 100;
my $d = -100;
my $e = 123_456_789; #Can use underscores like in python to make numbers more readable
my $f = 10.25;

print("Some sample numbers: C: $c. D: $d. E: $e. F: $f.\n");

#Binary, Hexadecimal, and Octal are supported (0b, 0x, 0 as prefixes to those numbers for conversions)

# Strings

my $s1 = "string with doubled-quotes"; # Note that single quotes treat what's inside as text where as double quotes treat whats inside like variables. This means you can't put variables inside the single quote strings.
my $s2 = 'string with single quote';

# Using q// and qq// act as single and double quotes, as an alternative so that you can use "" in the strings
my $str1 = q/"Inspirational Quote" -Mahatma Ghandi./;

my $name = 'Jack';
my $str2 = qq/"Secondary Quote"-$name./;
print($str1 ,"\n");
print($str2 ,"\n");

# Find the length of a string
my $string_length = length($name);
print("The length of the name string is: $string_length.\n");

# Changing the (upper/lower)case of a string
my $case_string = "uP aNd DoWn";
print("Upper case: ", uc($case_string), ". Lower case: ", lc($case_string), ".\n");

# Index Methods
my $full_string = "Life is full of ups and downs";
my $sub = "full";
my $str_index = index($full_string, $sub); # rindex is the same but searches from right to left. #Returns an int (Starting pos)

print("The index of $sub in $full_string is $str_index.\n");

# Sub strings
my $sentence = "Green is my favorite color";
my $color = substr($sentence, 0, 5); # Green
my $end = substr($sentence, -5); # color

print($end," : ",$color,"\n");

# replace substring
substr($sentence, 0, 5, "Red"); #Red is my favorite color
print($sentence,"\n");

#Potentially Useful Functions
# chr (Int -> ASCII char)
# ord (ASCII char -> Int)
# reverse (reverses the string)
# sprintf (string formatter)

# Logical Operators
# && and operator
# || or operator
# !(var) logical not




