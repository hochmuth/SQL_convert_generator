#! /bin/bash

extension='txt'

for f in ./*.$extension
do	
	wc -l $f
done
