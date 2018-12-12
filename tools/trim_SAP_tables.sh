#!/bin/bash
if [[ $# > 1 ]]; then
	echo "Usage: ./trimAndClean.sh [path/to/files/]"
	exit
fi

if [[ $# = 0 ]]; then
	DIRECTORY="."
else
	DIRECTORY="${1}"
fi

if [ ! -d "$DIRECTORY/converted" ]; then
	mkdir "$DIRECTORY/converted"
fi
shopt -s nullglob
for f in "${DIRECTORY}/"*.txt

do
	echo "Processing $(basename "$f") file..."
	# posledny regex je sporny, odstranuje znak na zaciatku + pipu (nemusi to fungovat spravne)
	sed -e '/^[^|]/d' -e 's/\s*|/|/g' -e 's/|\s*/|/g' -e 's/|$//' -e 's/^.|//' "${f}"  > "${DIRECTORY}/converted/$(basename "$f")"
	
done 