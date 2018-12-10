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
	done
	
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

# LOOPS
<< --COMMENT--
for i in *.txt
do
	echo $i
	mv $i $i.old # create backups
	sed 's/Atlanta/&, the capital of the South/' < $i.old > $i
done
--COMMENT--

pattern=...
while [ -n "$string" ]
do
	string=${string%$pattern}
	echo $string
done

<< --COMMENT--
printf "Enter username: "
read user
while true
do
	if who | grep "$user" > /dev/null
	then
		echo 'no, sorry'
		break
	fi
	
	echo 'yeah'
	break
done
--COMMENT--


while IFS=: read user pass uid gid fullname homedir shell
do
	continue	
done < /etc/passwd # needs to be here (after the loop) so that the file is opened only once



