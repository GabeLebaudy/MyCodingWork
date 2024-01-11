# This file will be smaller, just to be used for the string regular expression. This is the main use of this programming language

#Modules
use strict;
use warnings;

# Regular Expression

my $sample_string = "The quick brown fox lept over the moon.";

print("Regular expression returns true if the string contains a substring.\n") if ($sample_string =~ /quick/);
#print($sample_string =~ /lept/); #Prints 1 if found, nothing if not

my @sample_list = ("Mother", "Father", "Child");

for (@sample_list) {
    print("$_\n") if ($_ =~ /er/); #Prints the element if it contains the sub-string "er"
}

# Matching Expressions that have 
my $sample_html = "</span>";

print("This is printed using the backslash before the character\n") if ($sample_html =~ /\//);
print("This is printed using the m character instead of forward slash\n") if ($sample_html =~ m"/");

# Case Sensitivity
print("This shouldn't print\n") if ($sample_string =~ /BrOwn/);
print("This highlights the 'i' modifier\n") if ($sample_string =~ /Brown/i);

# Repeated Characters
my $sample_repeat = "a" x 100;

print("This string has 100 a's\n") if ($sample_repeat =~ /a{100}/);

# Useful quantifiers
# A* Zero or more A's (Idk when this wouldn't be true, doesn't seem too useful)
# A+ One or more A's
# A? A is optional (Same as A* idk when this would be false)
# A {10} Contains 10 A's
# A {1, 5} Contains between 1 and 5 A's
# A {2, } Contains 2 or more A's

# Example of modifiers above
my @modifer_list = ("available", "avatar", "avalon", "lion");
for (@modifer_list) {
    print("$_\n") if ($_ =~ /a*l+/); #Prints if the word contains zero or more a's followed by one or more l's (a part doesn't really do anything)
}

# To check for any of these characters {}[]()^$.|*+?\ You need to use a backslash before and after the character

# Regex Character Classes

my @animal_list = ("cat", "dog", "frog", "cow", "fog");

for (@animal_list) {
    print("$_\n") if ($_ =~ /[drf]og/); #Checks for dog, fog, frog, rog etc. (Characters in brackets can be used anywhere)
}

print("Number Range Example\n") if ("element1" =~ /element[0-1000]/); #Matches element0, element1 ... element1000
print("Letter Range Example\n") if ("g1" =~ /[a-z]1/);

# Pre-defined abbreviations for common character classes
# \d matches a digit 0-9
# \s matches a whitespace character
# \w matches a word

# \D matches a non digit 0-9
# \S matches any non-whitespace character
# \W matches any non-word


# Extracting Matches

my $extract_string = "This String Will Have No Whitespace!\n";
my $new_extract = $1 if ($extract_string =~ /(\S+)/);
print($new_extract, "\n");

# Alternation

print("Matched Apple\n") if "apple and orange" =~ /apple|orange|mango/; #| Character used to separate sequences of characters
print("Matched Orange\n") if "apple and orange" =~ /orange|apple|mango/; 

# Grouping

print("Matched Firefighter\n") if "Firefighter" =~ /Fire(fighter|man|woman)/;
print("Matched Firewoman\n") if "Firewoman" =~ /Fire(fighter|man|woman)/;

# Substitution and Translation

my $substitution_string = "This string will be used for substitution\n";
$substitution_string =~ s/string/sentence/;
print($substitution_string);

my $second_sub_string = "This Sentence Will Have No Whitespace\n";
$second_sub_string =~ s/ //g; #You can combine 'g' and 'i' together to replace all occurances regardless of character case
print($second_sub_string);

