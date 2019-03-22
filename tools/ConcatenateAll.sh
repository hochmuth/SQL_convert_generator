# Should take all text files in a folder and concatenate them into one, 
# while maintaining only one header (from the first file).
# Arguments should be as follows: 
#	directory
#	extension
#	output file name

# Logic
# Open the first file, read the first line (header) and store inside a string
# Write the header into the output file (?)
# For all files:
#	Open the file, remove the header, and copy (append) the rest into the output file


# Should probably create a new folder to store the newly created file.

# Ideas
# First write the header (first line), then everything else 
# head -1 file.txt > all.txt && tail -n +2 -q >> all.txt

# Or
# head -n1 file1.txt > combined.txt
# for fname in *.txt
# do
# 	    tail -n+2 $fname >> combined.txt
# done

# Store all files in an array; write the header from the first one; for all the rest append all expect the header

# Arguments
extension='csv'

if [[ $# = 0 ]]; then
	directory="."
else
	directory="${1}"
fi


# Create necessary folder
if [-d "$directory/joined_file" ] ; then
	echo "Can't create folder. Folder already exists."
	exit 1
fi

if [ ! -d "$directory/joined_file" ] ; then
	mkdir "$directory/joined_file"
fi


# Heavy lifting
array=("${directory}/"*."${extension}" ) && 
	head -1 ${array[0]} > "${directory}/joined_file/result.csv" &&
       	tail -n +2 -q ${array[@]:0} >> "${directory}/joined_file/result.csv"
