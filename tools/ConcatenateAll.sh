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



# Ideas
# First write the header (first line), then everything else 
head -1 file.txt > all.txt && tail -n +2 -q >> all.txt

# Or
head -n1 file1.txt > combined.txt
for fname in *.txt
do
	    tail -n+2 $fname >> combined.txt
done

# Store all files in an array; write the header from the first one; for all the rest append all expect the header

array=( *.txt );head -1 ${array[0]} > all.txt; tail -n +2 -q ${array[@]:0} >> all.txt
