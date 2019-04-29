


if [ -d "./01_delimiters" ] ; then
	rm -rf ./01_delimiters
fi

if [ -d "./02_encoding" ] ; then
	rm -rf ./02_encoding
fi

if [ "$(ls -A | grep -i \\.csv\$)" ] ; then
	rm *.csv
fi

if [ "$(ls -A | grep -i \\.log\$)" ] ; then
	rm *.log
fi

if [ "$(ls -A | grep -i \\.sql\$)" ] ; then
	rm *.sql
fi

if [ "$(ls -A | grep -i \\.txt\$)" ] ; then
	rm *.txt
fi
