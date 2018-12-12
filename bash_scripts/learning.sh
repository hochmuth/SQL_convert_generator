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

# CUT
# Selects only the first and fifth field from the passwd file, finds the line with my username and prints only the first five matches
cut -d : -f 1,5 /etc/passwd | grep es579dx | head -n 5

# list only permissions
ls -l | cut -c 1-10

# AWK
#print username and full name from the passwd file

awk -F: '{ print "User", $1, "is really", $5 }' /etc/passwd

# SORT
# sort passwd by username, desc
sort -t: -k1,1 /etc/passwd

# UNIQ
# removes duplicates
sort /etc/passwd | uniq

# count unique sorted records
sort /etc/passwd | uniq -c

# show only duplicates
sort /etc/passwd | uniq -d

# show only unique records
sort /etc/passwd | uniq -u

# COUNT

echo Testing one two three | wc -c # count bytes
echo Testing one two three | wc -l # count lines
echo Testing one two three | wc -w # count words

# READONLY
hours_per_day = 24
readonly hours_per_day # makes the variable read-only

# EXPORT
# adds new variables into the environment
export PATH
export -p # prints the current environment

# UNSET removes variables and functions from the running shell
who_is_on () {
	who | awk '{ print $1 }' | sort -u
}
unset -f who_is_on

# VARIABLES
reminder="Time to go to the dentist!"
echo $reminder
echo _${reminder}_

# BASENAME
# returns filename stripped of path, etc.
basename /etc/passwd

# COMPARING FILES
# cmp file1 file2	# silent
# diff file1 file2	# shows the differences

