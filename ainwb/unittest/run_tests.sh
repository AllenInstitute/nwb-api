#!/bin/bash
FILES=y_*py
for f in $FILES
	do
		python $f || >&2 echo "$f FAILED"
	done

