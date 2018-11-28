#! /bin/bash

printf "The first program you write is always '%s %s'!\n" hello world

for f in *.txt
do
	tr -d '\r' < $f >> test_output.txt
done

