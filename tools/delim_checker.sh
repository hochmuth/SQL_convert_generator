#!/bin/bash

log_file=errors.log
encoding='utf-16-le'
delim='|'
extension='txt'

if [[ $# > 1 ]] ; then
	echo "Too many arguments. Usage: ./delim_checker.sh (path)"
	exit
fi

# Get directory
if [[ $# = 0 ]] ; then
	DIRECTORY="."
else
	DIRECTORY="${1}"
fi

# Log file
if [ -f $log_file ] ; then
	rm $log_file
fi

echo 'Processing files...' > $log_file
echo >> $log_file

# Main loop
for f in "${DIRECTORY}/"*."${extension}"
do
	echo "Processing $(basename "$f") file" >> $log_file
	csvclean -e $encoding -d $delim --quoting 3 --dry-run $f >> $log_file	
	echo >> $log_file
done

unix2dos errors.log

exit 
