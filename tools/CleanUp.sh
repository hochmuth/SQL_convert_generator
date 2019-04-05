


if [ -d "./01_delimiters" ] ; then
	rm -rf ./01_delimiters
fi

if [ -d "./02_encoding" ] ; then
	rm -rf ./02_encoding
fi

if [ -f *.csv ] ; then
	rm *.csv
fi

if [ -f *.log ] ; then
	rm *.log
fi
