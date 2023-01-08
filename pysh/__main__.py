#!/usr/bin/env python3

import traceback
import subprocess
from io import BytesIO
import os

def cd(path):
	try:
		os.chdir(path)
	except Exception as e:
		print(traceback.format_exc())
		return

def cmd(line):
	split = line.split()
	if split[0] == "cd":
		cd(split[1])
		return
	try:
		subprocess.run(split)
	except:
		print(traceback.format_exc())
		return

def get_bins():
	result = []
	for path in os.environ["PATH"].split(":"):
		try:
			for b in os.listdir(path):
				result.append(b)
		except Exception as e:
			print(traceback.format_exc())
	return result

bins = set(get_bins())
print(len(bins))
shident = ["cd"]

def proc(line):
	tok1 = line.split()
	if not tok1:
		return
	tok1 = tok1[0]
	if tok1 in shident or tok1 in bins:
		cmd(line)
	else:
		exec(line)

while True:
	line = input("> ")
	proc(line)
