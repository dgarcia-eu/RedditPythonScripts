#!/usr/bin/python
import sys

jsonfilename = str(sys.argv[1])
fin = open(jsonfilename, "rt")

for line in fin:
	fields = line.split(",")
	for field in fields:
		if '"author"' in field:
			content = field.split(":")
			username = content[1].replace('"', '').strip()
			print username
