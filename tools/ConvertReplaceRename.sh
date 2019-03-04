#	Replaces unicode delimiters in text files with pipes
#	and then converts the resulting files into UTF-16 Big Endian.
#
#	Directories created:
#   01_delimiters - files with delimiters replaced
#   02_encoding - converted to UTF-16

extension='csv'


if [[ $# > 1 ]]; then
	echo "Usage: ./ConvertTextFiles.sh [path/to/files/]"
	exit
fi

if [[ $# = 0 ]]; then
	DIRECTORY="."
else
	DIRECTORY="${1}"
fi

if [ -d "$DIRECTORY/01_delimiters" ] || [ -d "$DIRECTORY/02_encoding" ] ; then
	echo "Can't create folder. Folder already exists."
	exit 1
fi

if [ ! -d "$DIRECTORY/01_delimiters" ] || [ ! -d "$DIRECTORY/02_encoding" ] ; then
	mkdir "$DIRECTORY/01_delimiters"
	mkdir "$DIRECTORY/02_encoding"
fi

# Rename the files
rename 's/[0-9]+(_).{3}(_)//' *."${extension}"

# Replace delimiters and convert encoding
for file in *."${extension}"; do
	sed -e "s/|/¦/g" -e "s/╬/|/g" "$file" > "./01_delimiters/$file"
  	iconv -f utf-8 -t utf-16BE "./01_delimiters/$file" > "./02_encoding/$file"
done
