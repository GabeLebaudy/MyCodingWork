# This file will be used for the next couple of lessons. Not sure if they will lead in OOP but will edit later.

# Modules
use strict;
use warnings;

# References

# Create a refrence
my $x = 10;
my $x_ref = \$x;

$$x_ref *= 2;

print($x, "\n");

# Array example

my @array = (1..10);
my $array_ref = \@array;

my $count = 0;
for (@$array_ref) {
    print("$array_ref->[$count++] \n");
}

# Subroutines (Functions)

sub hello_world {
    print("Hello World!\n");
}

# Can call functions one of two ways
&hello_world;
hello_world();

sub sum {
    my $total = 0;
    for my $i(@_) {
        $total += $i;
    }
    return $total;
}

print sum(@array, "\n");

my $val1 = 1;
my $val2 = 2;

# Passing in parameters by reference (Modifies variables)
sub sample_method {
    $_[0] = 10;
    $_[1] = 20;
}

&sample_method;

print("The values after the method are $val1 $val2\n");

# Passing in parameters by value

my $val3 = 100;
my $val4 = 200;

sub sample_value {
    my ($v1, $v2) = @_;
    $v1 = 1;
    $v2 = 2;
}

&sample_value;

print("The values after the method are $val3 $val4\n");

