#! /bin/bash

printf "The first program you write is always '%s %s'!\n" hello world

for f in *.txt
do
	tr -d '\r' < $f > test_output.txt
done

# removes the carriage return, then sorts, then saves into a new file
#for f in *.txt
#do
#	tr -d '\r' < $f | sort > unix-file.txt
#done

# Tip - when constructing pipelines, the amount of data should be reduced at each stage. Improves the efficiency. 
# For example, first use grep to select lines you want, and only then apply sort.

echo $PATH

# Find user ---- see if user named by first argument is logged in
#who | grep $1

# Execution tracing works like this:
set -x		#turn tracing on
who | wc -l
set +x		# turn tracing off

# GREP

who | grep marvin
