# WORKING WITH FILES

umask 077						# remove access for all but the user
TMPFILE=`mktemp /tmp/myprog.XXXXXXXXXXXX` || exit 1	# make unique temporary file with a random name (or exit immediately in case of an error)
ls -l $TMPFILE

trap 'exit 1'          HUP INT PIPE QUIT TERM
trap 'rm -f $TMPFILE' EXIT				# trap command ensures that the temp file is removed when the script terminates

exit
