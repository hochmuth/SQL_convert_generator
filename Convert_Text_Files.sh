#	Replaces unicode delimiters in text files with pipes
#	and then converts the resulting files into UTF-16 Big Endian.
#
#	Directories created:
#   01_delimiters - files with delimiters replaced
#   02_encoding - converted to UTF-16

mkdir ./01_delimiters
mkdir ./02_encoding

for file in *.csv; do
  sed -e "s/|/¦/g" -e "s/╬/|/g" "$file" > "./01_delimiters/$file"
  iconv -f utf-8 -t utf-16BE "./01_delimiters/$file" > "./02_encoding/$file"
done
