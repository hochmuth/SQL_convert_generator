#!/bin/bash

log_file=errors.log
encoding='utf-16'
delim='|'

if [ -f $log_file ] ; then
	rm $log_file
fi

echo 'Processing files...' > $log_file
echo >> $log_file

for f in ./*.txt
do
	echo "Processing $(basename "$f") file" >> $log_file
	csvclean -e $encoding -d $delim --quoting 3 --dry-run $f >> $log_file	
	echo >> $log_file
done

unix2dos errors.log
