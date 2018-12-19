#!/bin/bash

extension='txt'

if [[ $# > 1 ]]; then
	echo "Usage: ./trimAndClean.sh [path/to/files/]"
	exit
fi

if [[ $# = 0 ]]; then
	DIRECTORY="."
else
	DIRECTORY="${1}"
fi

if [ -d "$DIRECTORY/01_trimmed" ] || [ -d "$DIRECTORY/02_pipes" ] || [ -d "$DIRECTORY/03_enc" ] ; then
	echo "Folder '01_trimmed' already exists."
	exit 1
fi

if [ ! -d "$DIRECTORY/01_trimmed" ] || [ ! -d "$DIRECTORY/02_pipes" ] || [ ! -d "$DIRECTORY/03_enc" ] ; then
	mkdir "$DIRECTORY/01_trimmed"
	mkdir "$DIRECTORY/02_pipes"
	mkdir "$DIRECTORY/03_enc"
fi

shopt -s nullglob

# First run for removing the white spaces and trailing 02_pipes
for f in "${DIRECTORY}/"*."${extension}"
do
	echo "Processing $(basename "$f") file..."
	# posledny regex je sporny, odstranuje znak na zaciatku + pipu (nemusi to fungovat spravne)
	sed -e '/^[^|]/d' -e 's/\s*|/|/g' -e 's/|\s*/|/g' -e 's/|$//' -e 's/^.|//' "${f}"  > "${DIRECTORY}/01_trimmed/$(basename "$f")"	
done 

# Second run for removing the leading 02_pipes
for f in "${DIRECTORY}/"01_trimmed/*."${extension}"
do
	echo "Removing leadin 02_pipes of $(basename "$f") file..."
	sed -e 's/^|//' "${f}"  > "${DIRECTORY}/02_pipes/$(basename "$f")"
done

# Third run for converting to UTF-16
for f in "${DIRECTORY}/"02_pipes/*."${extension}"
do
	echo "Converting encoding of $(basename "$f") file..."
	iconv -f utf-8 -t utf-16 "${f}" > "${DIRECTORY}/03_enc/$(basename "$f")"
done
