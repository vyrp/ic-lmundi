#!/bin/sh
#
# Add the following line to ./.git/hooks/pre-commit just before the final 'exec':
# . ./pre_commit.sh

flake8 .
if [ $? -ne 0 ]; then
	echo "Error: did not pass Flake8 validation."
	exit 1
fi

PYTHONPATH="C:\Program Files (x86)\Google\google_appengine" python test.py
if [ $? -ne 0 ]; then
	echo "Error: Python code not valid."
	exit 1
fi
