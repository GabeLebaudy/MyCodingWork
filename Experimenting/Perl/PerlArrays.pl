#This file will contain information about perl lists, arrays, and hashmaps

#Modules
use strict;
use warnings;

# Lists
(); # Empty list
print(1, 2, 3);  #Simple list, prints 123. All one data type
print("\n");

my $number = 10;
my $word = " Example ";

print("Complex ", $number, $word, 10.25, "\n"); #Comlpex list, contains multiple data types

# Qw
print('a', 'b', 'c', "\n"); #Prints abc, as list
print(qw(a b c), "\n"); #Also prints abc, but qw automatically uses the space delimeter to create a list

# Perl automatically flattens lists, for example (1, 2, (3, 4)) = (1, 2, 3, 4)

# Indexing a list
print((1, 2, 3)[0], "\n"); #Prints first element
print((1, 2, 3, 4)[0, 2], "\n"); #You are able to select multiple items at a time

# Ranges
print(1..10, "\n"); #Prints 1-10
print("a".."g", "\n"); #Prints a-g

# Arrays
my @array = (1, 2, 3, 4, 5, 6, 7);
print("My array: @array.\n");

# Indexing an array
print("Item at index 0: ", $array[0], "\n");

my @sub_array = @array[-3..-1]; #3rd to last, to last items are stored in this array
print("Subsection of array: @sub_array.\n");

my $arr_length = scalar @array; #Easy way to get length of an array
print("Length of array: $arr_length.\n");

my $highest_index = $#array; #Returns the highest index of an array
print("The highest index of the array is: $highest_index.\n");

# Modifying elements in an array
$array[0] = 8;
print("Array after modifications: @array.\n");

@array[1..$highest_index] = qw(9 10 11 12 13 14);
print("Array after more changes: @array.\n");

# Push and pop elements (Treat array as stack)
push(@array, 15);
print("New array: @array.\n");

my $element = pop(@array);
print("The popped element was $element.\n");
print("New array @array.\n");

# Unshift and pop elements (Treat array as queue)
unshift(@array, 7);
print("Array after unshifting @array.\n");

my $new_element = pop(@array);
print("Popped element: $new_element.\n");
print("New Array @array.\n");

# Sort an array
my @unsorted = (4, 2, 0, 190, 328, 1, 3);
my @sorted = sort {$a <=> $b} @unsorted; #The bracket block is to force the array to sort numerically. Currently, it sorts by the first digit

print("Unsorted array: @unsorted.\n");
print("Sorted array: @sorted.\n");

# Hash maps (Dictionaries)

my %dictionary = ("England" => "English", "France" => "French", "Spain" => 'Spanish', "China" => 'Chinese', "Germany" => 'German');
my $first_lang = $dictionary{"England"};
print("The first language in the dictionary is: $first_lang.\n");

# Add/Modify an element element
$dictionary{"Italy"} = "Italian"; #Creates new element if key does not exist, modifies if it does.

# Delete an element
delete $dictionary{"China"};

# Print an entire dictionary
for (keys %dictionary) {
    print("Official language of $_ is $dictionary{$_}.\n");
}












