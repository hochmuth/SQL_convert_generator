# Command line arguments

echo first arg is $1
echo tenth arg is ${10} # greater than 9 needs to be enclosed in braces

echo was the second argument given? ${2:-no} # if null, prints 'no'

echo total number of args is $#

if  [ $# == 0 ]
then
	echo no arguments given
	echo setting my own arguments
	set -- hello "hi there" greetings
	echo there are now $# total args
	for i in $*
	do
		echo i is $i
	done
	for i in "$*"
	do
		echo i is $i
	for i in "$@"
	do echo i is $i
	done
	shift # lop off the first arg
	echo there are now $# arguments
	for i in "$@"
	do 
		echo i is $i
	done
fi
