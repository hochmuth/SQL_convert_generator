# Should take all text files in a folder and concatenate them into one, 
# while maintaining only one header (from the first file).
# Arguments should be as follows: 
#	directory
#	output file name

# Ideas
#
# head -n1 file1.txt > combined.txt
# for fname in *.txt
# do
# 	    tail -n+2 $fname >> combined.txt
# done

# Parameters
extension='txt'

# Deal with arguments
if [[ $# = 1 ]] || [[ $# > 2 ]]; then
	echo "Usage: ./ConcatenateAll.sh (directory out_file_name)"
	exit 2
fi

if [[ $# = 0 ]]; then
	out_file="out_file.${extension}"
else
	out_file="${2}"
fi

if [[ $# = 0 ]]; then
	directory="."
else
	directory="${1}"
fi

# Create the output folder
if [ -d "$directory/joined_file" ] ; then
	echo "Can't create folder. Folder already exists."
	exit 1
fi

if [ ! -d "$directory/joined_file" ] ; then
	mkdir "$directory/joined_file"
fi


# Heavy lifting
array=( "${directory}/"*."${extension}" ) && 
	head -1 ${array[0]} > "${directory}/joined_file/${out_file}" &&
       	tail -n +2 -q ${array[@]:0} >> "${directory}/joined_file/${out_file}"

exit 0
