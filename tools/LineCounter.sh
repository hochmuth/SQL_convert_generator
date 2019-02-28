#! /bin/bash

extension='txt'

if [[ $# > 1 ]] ; then
	echo "Too many arguments. Usage: ./lince_counter.sh (path)"
	exit
fi

# Get directory
if [[ $# = 0 ]] ; then
	directory="."
else
	directory="${1}"
fi

# Main loop
for f in "${directory}/"*.${extension}
do	
	wc -l $f
done

exit 0
