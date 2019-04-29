#	Accepts text files extracted from SAP with SmartExporter, and:
#		- deletes the SE log files (folder clean-up)
#		- renames the file names so that they match the table names (MSEG.csv etc.)
#		- replaces the Unicode delimiters with pipes (|)
#		- converts from UTF-8 to UTF-16 Big Endian
#
#	Folders created:
#   01_delimiters 	- files with replaced delimiters
#   02_encoding 	- converted to UTF-16

extension='csv'

# Check args
if [[ $# > 1 ]]; then
	echo "Usage: ./ConvertTextFiles.sh [path/to/files/]"
	exit 1
fi

if [[ $# = 0 ]]; then
	directory="."
else
	directory="${1}"
fi

# Create necessary folders
if [[ -d "$directory/01_delimiters" ]] || [[ -d "$directory/02_encoding" ]] ; then
	echo "Can't create folder. Folder already exists."
	exit 1
fi

if [[ ! -d "$directory/01_delimiters" ]] || [[ ! -d "$directory/02_encoding" ]] ; then
	mkdir "$directory/01_delimiters"
	mkdir "$directory/02_encoding"
fi

# Delete the log files if any
if [[ -f *.log ]]; then
	rm *.log
fi

# Rename the files
rename 's/[0-9]{14}(_).{3}(_)//' "${directory}/"*."${extension}"

# Replace delimiters and convert encoding
if [ "$(ls -A | grep -i \\.$extension\$)" ] ; then
	for file in "${directory}/"*."${extension}"; do
		sed -e "s/|/¦/g" -e "s/╬/|/g" "$file" > "${directory}/01_delimiters/$file"
  		iconv -f utf-8 -t utf-16BE "${directory}/01_delimiters/$file" > "${directory}/02_encoding/$file"
	done
else echo "No relevant files found."
	exit 0
fi

exit 0
