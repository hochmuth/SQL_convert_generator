#! /bin/bash

#mkdir ./encoding

if [[ $# > 1 ]] ; then
	echo "Usage ./convert.sh [path to files]"
	exit
fi

if [[ $# = 0 ]] ; then
	directory="."
else
	directory="${1}"
fi

if [ ! -d "$directory/encoding" ]; then
	mkdir "$directory/encoding"
fi

for file in "${directory}/"*.txt 
do
	iconv -f utf16LE -t utf16 $file | unix2dos > "${directory}"/encoding/$file
	
done
