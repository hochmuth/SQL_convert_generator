# Command line arguments

echo first arg is $1
echo tenth arg is ${10} # greater than 9 needs to be enclosed in braces

echo was the second argument given? ${2:-no} # if null, prints 'no'
